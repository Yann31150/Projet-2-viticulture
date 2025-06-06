from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import time
import json
import pandas as pd
from datetime import datetime
import random
import logging
from urllib.parse import urljoin
import undetected_chromedriver as uc
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from tqdm import tqdm
import os

# Configuration du logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraping.log'),
        logging.StreamHandler()
    ]
)

def setup_driver():
    """Configure le driver Selenium avec les options appropriées"""
    try:
        # Utilisation de undetected_chromedriver pour éviter la détection
        options = uc.ChromeOptions()
        # Désactiver le mode headless qui peut causer des problèmes
        # options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Génération d'un User-Agent aléatoire
        ua = UserAgent()
        options.add_argument(f'--user-agent={ua.random}')
        
        # Ajout d'arguments supplémentaires pour éviter la détection
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--disable-save-password-bubble')
        options.add_argument('--disable-translate')
        options.add_argument('--disable-web-security')
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--no-first-run')
        options.add_argument('--no-service-autorun')
        options.add_argument('--password-store=basic')
        options.add_argument('--use-mock-keychain')
        
        # Création du driver avec undetected_chromedriver
        driver = uc.Chrome(options=options)
        driver.implicitly_wait(15)
        
        # Configuration de la taille de la fenêtre
        driver.set_window_size(1920, 1080)
        
        # Ajout de cookies pour simuler une session utilisateur
        driver.get("https://www.vinatis.com")
        time.sleep(random.uniform(2, 4))
        
        # Exécution de JavaScript pour masquer les traces d'automatisation
        driver.execute_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)
        
        # Créer le dossier pour les fichiers de debug
        os.makedirs('debug', exist_ok=True)
        
        logging.info("Driver configuré avec succès")
        
    except Exception as e:
        logging.error(f"Erreur lors de la configuration du driver: {str(e)}")
        raise
    return driver

class VinatisScraper:
    def __init__(self):
        self.driver = None
        self.base_url = "https://www.vinatis.com"
        self.data = []
        self.visited_urls = set()
        self.categories = {
            'rouge': '/vin-rouge',
            'blanc': '/vin-blanc',
            'rose': '/vin-rose',
            'champagne': '/champagne',
            'spiritueux': '/spiritueux'
        }

    def accept_cookies(self):
        """Accepte les cookies sur le site, essaie plusieurs sélecteurs."""
        selectors = [
            (By.ID, "onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, "#onetrust-button-group #onetrust-accept-btn-handler"),
            (By.CSS_SELECTOR, ".ot-sdk-container button#onetrust-accept-btn-handler"),
            (By.XPATH, "//button[contains(@id, 'onetrust-accept-btn-handler')]"),
            (By.XPATH, "//button[contains(text(), 'Accepter') or contains(text(), 'Tout accepter')]"),
            (By.CSS_SELECTOR, ".ot-sdk-container .ot-sdk-row button")
        ]
        
        # Attendre que la page soit complètement chargée
        time.sleep(random.uniform(3, 5))
        
        accepted = False
        for by, value in selectors:
            try:
                logging.info(f"Recherche du bouton cookies avec {by}={value}")
                
                # Attendre que le bouton soit cliquable
                cookie_button = WebDriverWait(self.driver, 30).until(
                    EC.element_to_be_clickable((by, value))
                )
                
                # Simuler un comportement humain avant de cliquer
                self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", cookie_button)
                time.sleep(random.uniform(0.5, 1.5))
                
                # Cliquer avec JavaScript pour éviter la détection
                self.driver.execute_script("arguments[0].click();", cookie_button)
                
                time.sleep(random.uniform(2, 4))
                logging.info("Bouton cookies cliqué avec succès.")
                accepted = True
                break
                
            except Exception as e:
                logging.info(f"Bouton cookies non trouvé avec {by}={value}: {e}")
                
        if not accepted:
            # Sauvegarde la page pour inspection
            with open('cookies_debug.html', 'w', encoding='utf-8') as f:
                f.write(self.driver.page_source)
            logging.warning("Aucun bouton cookies trouvé. Page sauvegardée sous cookies_debug.html.")

    def get_product_links(self, category_url, max_pages=5):
        """Récupère les liens des produits d'une catégorie"""
        product_links = set()
        page = 1
        
        while page <= max_pages:
            try:
                url = f"{category_url}?page={page}"
                logging.info(f"Analyse de la page {page} de la catégorie {category_url}")
                
                # Chargement de la page avec un comportement plus humain
                self.driver.get(url)
                accept_cookies(self.driver)
                time.sleep(random.uniform(4, 6))
                
                # Simulation du défilement de la page
                self.simulate_human_scroll()
                
                # Attendre que la page soit complètement chargée
                WebDriverWait(self.driver, 30).until(
                    EC.presence_of_element_located((By.TAG_NAME, "body"))
                )
                
                # Attendre que le contenu dynamique soit chargé
                try:
                    WebDriverWait(self.driver, 20).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, ".product-list, .product-grid, .product-items, .product-card"))
                    )
                except TimeoutException:
                    logging.warning("Le contenu des produits n'a pas été trouvé dans le délai imparti")
                
                time.sleep(random.uniform(3, 5))
                
                # Vérifier si la page existe
                if "Page non trouvée" in self.driver.page_source:
                    logging.info("Page non trouvée, fin de la pagination")
                    break
                
                # Essayer différents sélecteurs pour trouver les produits
                selectors = [
                    ".product-card a.product-link",
                    ".product-item a.product-link",
                    ".product-list a[href*='/vin-']",
                    ".product-grid a[href*='/vin-']",
                    "a[href*='/vin-'][data-testid='product-link']",
                    ".product-items a[href*='/vin-']",
                    ".product-card a[href*='/vin-']",
                    "a.product-link[href*='/vin-']",
                    ".product-item a[href*='/vin-']",
                    "a[href*='/vin-'][class*='product']",
                    ".product a[href*='/vin-']"
                ]
                
                product_elements = []
                for selector in selectors:
                    try:
                        # Attendre que les éléments soient présents
                        elements = WebDriverWait(self.driver, 10).until(
                            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
                        )
                        if elements:
                            product_elements = elements
                            logging.info(f"Produits trouvés avec le sélecteur: {selector}")
                            break
                    except Exception as e:
                        logging.info(f"Sélecteur {selector} non trouvé: {str(e)}")
                
                logging.info(f"Nombre de produits trouvés sur la page {page}: {len(product_elements)}")
                
                if not product_elements:
                    # Sauvegarder la page pour inspection
                    with open(f'debug/page_debug_{page}.html', 'w', encoding='utf-8') as f:
                        f.write(self.driver.page_source)
                    logging.info(f"Aucun produit trouvé sur la page {page}, page sauvegardée pour inspection")
                    break
                
                # Récupérer les liens des produits
                for element in product_elements:
                    try:
                        # Faire défiler jusqu'à l'élément
                        self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
                        time.sleep(random.uniform(0.1, 0.3))
                        
                        href = element.get_attribute('href')
                        if href and '/vin-' in href and href not in self.visited_urls:
                            product_links.add(href)
                            self.visited_urls.add(href)
                            logging.info(f"Nouveau lien trouvé: {href}")
                    except Exception as e:
                        logging.error(f"Erreur lors de la récupération du lien: {str(e)}")
                
                page += 1
                
            except Exception as e:
                logging.error(f"Erreur lors de la récupération des liens de la page {page}: {str(e)}")
                break
        
        return product_links

    def simulate_human_scroll(self):
        """Simule un défilement humain de la page"""
        try:
            # Obtenir la hauteur totale de la page
            total_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Défiler progressivement
            current_position = 0
            scroll_step = random.randint(100, 300)
            
            while current_position < total_height:
                # Défiler d'une distance aléatoire
                current_position += scroll_step
                self.driver.execute_script(f"window.scrollTo(0, {current_position});")
                
                # Attendre un temps aléatoire entre chaque défilement
                time.sleep(random.uniform(0.1, 0.3))
                
                # Parfois, faire une pause plus longue
                if random.random() < 0.1:
                    time.sleep(random.uniform(0.5, 1.5))
            
            # Remonter en haut de la page
            self.driver.execute_script("window.scrollTo(0, 0);")
            time.sleep(random.uniform(1, 2))
            
        except Exception as e:
            logging.error(f"Erreur lors du défilement de la page: {str(e)}")

    def scrape_wine_page(self, url):
        """Scrape les informations d'une page de vin"""
        try:
            self.driver.get(url)
            accept_cookies(self.driver)
            time.sleep(5)  # Attente initiale pour le chargement de la page
            
            # Attendre que la page soit complètement chargée
            WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Attendre que le contenu du produit soit chargé
            try:
                WebDriverWait(self.driver, 20).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".product-details, .product-info, .product-main-info"))
                )
            except TimeoutException:
                logging.warning("Le contenu du produit n'a pas été trouvé dans le délai imparti")
            
            time.sleep(random.uniform(3, 5))

            # Log de la page source pour le débogage
            logging.info(f"Page source de {url}: {self.driver.page_source[:500]}...")

            wine_data = {
                'url': url,
                'nom': self.get_text_safe('.product-title, [data-testid="product-title"], .product-main-info h1'),
                'prix': self.get_text_safe('.product-price, [data-testid="product-price"], .price-box .price'),
                'region': self.get_text_safe('.product-region, [data-testid="product-region"], .product-details .region'),
                'cepage': self.get_text_safe('.product-grapes, [data-testid="product-grapes"], .product-details .grapes'),
                'description': self.get_text_safe('.product-description, [data-testid="product-description"], .product-details .description'),
                'millesime': self.get_text_safe('.product-vintage, [data-testid="product-vintage"], .product-details .vintage'),
                'alcool': self.get_text_safe('.product-alcohol, [data-testid="product-alcohol"], .product-details .alcohol'),
                'volume': self.get_text_safe('.product-volume, [data-testid="product-volume"], .product-details .volume'),
                'note': self.get_text_safe('.product-rating, [data-testid="product-rating"], .product-details .rating'),
                'stock': self.get_text_safe('.product-stock, [data-testid="product-stock"], .product-details .stock'),
                'categorie': self.get_text_safe('.breadcrumb, [data-testid="breadcrumb"], .breadcrumbs'),
                'date_scraping': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
            
            # Log des données récupérées
            logging.info(f"Données récupérées pour {url}: {json.dumps(wine_data, ensure_ascii=False)}")
            
            self.data.append(wine_data)
            return wine_data

        except Exception as e:
            logging.error(f"Erreur lors du scraping de {url}: {str(e)}")
            return None

    def get_text_safe(self, selector):
        """Récupère le texte d'un élément de manière sécurisée"""
        try:
            # Essayer d'abord avec WebDriverWait
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, selector))
            )
            text = element.text.strip()
            if text:
                logging.info(f"Texte trouvé pour {selector}: {text}")
                return text
            return None
        except (NoSuchElementException, TimeoutException):
            logging.info(f"Élément non trouvé pour le sélecteur: {selector}")
            return None
        except StaleElementReferenceException:
            logging.info(f"Élément périmé pour le sélecteur: {selector}")
            return None
        except Exception as e:
            logging.error(f"Erreur inattendue pour le sélecteur {selector}: {str(e)}")
            return None

    def save_to_json(self, filename='vinatis_data.json'):
        """Sauvegarde les données au format JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        logging.info(f"Données sauvegardées dans {filename}")

    def save_to_csv(self, filename='vinatis_data.csv'):
        """Sauvegarde les données au format CSV"""
        df = pd.DataFrame(self.data)
        df.to_csv(filename, index=False, encoding='utf-8')
        logging.info(f"Données sauvegardées dans {filename}")

    def scrape_category(self, category_name, max_pages=5, max_products=50):
        """Scrape une catégorie complète de vins"""
        if category_name not in self.categories:
            logging.error(f"Catégorie {category_name} non trouvée")
            return
        
        category_url = urljoin(self.base_url, self.categories[category_name])
        logging.info(f"Début du scraping de la catégorie {category_name}")
        
        product_links = self.get_product_links(category_url, max_pages)
        product_links = list(product_links)[:max_products]
        
        logging.info(f"Nombre total de liens trouvés pour {category_name}: {len(product_links)}")
        
        for i, url in enumerate(product_links, 1):
            logging.info(f"Scraping du produit {i}/{len(product_links)}")
            self.scrape_wine_page(url)
            time.sleep(random.uniform(1, 3))

    def close(self):
        """Ferme le driver"""
        if self.driver:
            self.driver.quit()

def get_product_links(driver, page):
    url = f"https://www.vinatis.com/?type%5B%5D=Vin&tri=7&page={page}"
    print(f"\nTentative d'accès à l'URL: {url}")
    
    max_retries = 3
    for attempt in range(max_retries):
        try:
            driver.get(url)
            accept_cookies(driver)
            # Attendre plus longtemps pour le chargement
            time.sleep(random.uniform(3, 5))
            
            # Vérifier si nous sommes sur la bonne page
            current_url = driver.current_url
            print(f"URL actuelle: {current_url}")
            
            # Afficher le titre de la page
            print(f"Titre de la page: {driver.title}")
            
            # Sauvegarder le HTML pour debug
            with open(f"debug/page_{page}.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print(f"HTML sauvegardé dans debug/page_{page}.html")
            
            soup = BeautifulSoup(driver.page_source, "html.parser")
            
            # Vérifier si nous avons des produits
            products = soup.select("div.product-container")
            print(f"Nombre de produits trouvés: {len(products)}")
            
            # Chercher les liens
            links = soup.select("a.product-thumbnail")
            print(f"Nombre de liens trouvés: {len(links)}")
            
            if not links:
                print("Aucun lien trouvé. Contenu de la page:")
                print(soup.prettify()[:1000])  # Afficher les 1000 premiers caractères
                if attempt < max_retries - 1:
                    print(f"Tentative {attempt + 1} échouée, nouvelle tentative...")
                    time.sleep(random.uniform(5, 10))
                    continue
            else:
                return ["https://www.vinatis.com" + link["href"] for link in links if link.get("href")]
                
        except Exception as e:
            print(f"Erreur lors de la tentative {attempt + 1}: {str(e)}")
            if attempt < max_retries - 1:
                print("Nouvelle tentative...")
                time.sleep(random.uniform(5, 10))
            else:
                print("Toutes les tentatives ont échoué")
                return []
    
    return []

def get_product_info(driver, product_url):
    try:
        print(f"\nRécupération des infos pour: {product_url}")
        driver.get(product_url)
        accept_cookies(driver)
        time.sleep(random.uniform(2, 4))  # Attente aléatoire
        
        soup = BeautifulSoup(driver.page_source, "html.parser")
        
        # Extraction du nom
        name_tag = soup.find("h1", class_="product-main-name")
        name = name_tag.get_text(strip=True) if name_tag else None
        print(f"Nom trouvé: {name}")
        
        # Extraction de l'image
        img_tag = soup.select_one("img#bigpic")
        image_url = img_tag["src"] if img_tag and img_tag.get("src") else None
        print(f"URL image trouvée: {image_url}")
        
        # Extraction de l'ID
        product_id = None
        if image_url:
            import re
            match = re.search(r"/(\d+)-thickbox_", image_url)
            if match:
                product_id = match.group(1)
        print(f"ID trouvé: {product_id}")
        
        return {
            "name": name,
            "id": product_id,
            "image_url": image_url,
            "url": product_url
        }
    except Exception as e:
        print(f"Erreur lors de la récupération des infos pour {product_url}: {str(e)}")
        return {"name": None, "id": None, "image_url": None, "url": product_url}

def scrape_all_products(n_pages=2, pause=1.0):
    driver = setup_driver()
    
    try:
        all_data = []
        for page in tqdm(range(1, n_pages + 1), desc="Scraping Vinatis"):
            print(f"\nTraitement de la page {page}/{n_pages}")
            links = get_product_links(driver, page)
            print(f"Nombre de liens trouvés sur la page {page}: {len(links)}")
            
            for link in links:
                info = get_product_info(driver, link)
                if info["id"] and info["name"]:
                    all_data.append(info)
                    print(f"Produit ajouté: {info['name']}")
                time.sleep(random.uniform(pause, pause * 2))
            
            # Sauvegarde intermédiaire tous les 10 pages
            if page % 10 == 0:
                df = pd.DataFrame(all_data)
                df.to_csv(f"vinatis_products_page_{page}.csv", index=False)
                print(f"\nSauvegarde intermédiaire effectuée à la page {page}")
        
        return pd.DataFrame(all_data)
    except Exception as e:
        print(f"Erreur lors du scraping: {str(e)}")
        return pd.DataFrame(all_data)
    finally:
        try:
            driver.quit()
        except:
            pass

def main():
    scraper = VinatisScraper()
    try:
        logging.info("Démarrage du scraper Vinatis")
        scraper.setup_driver()
        logging.info("Driver configuré avec succès")
        
        # Accéder à la page d'accueil
        scraper.driver.get(scraper.base_url)
        logging.info("Page d'accueil chargée")
        
        # Accepter les cookies
        scraper.accept_cookies()
        logging.info("Gestion des cookies terminée")
        
        # Attendre un peu après l'acceptation des cookies
        time.sleep(5)
        
        # Test avec une seule catégorie pour le débogage
        category = 'rouge'
        logging.info(f"Début du scraping de la catégorie {category}")
        scraper.scrape_category(category, max_pages=2, max_products=10)
        
        # Vérifier si des données ont été collectées
        if scraper.data:
            logging.info(f"Nombre de produits scrapés: {len(scraper.data)}")
            # Sauvegarde des données
            scraper.save_to_json()
            scraper.save_to_csv()
        else:
            logging.warning("Aucune donnée n'a été collectée")

    except Exception as e:
        logging.error(f"Une erreur est survenue: {str(e)}")
    finally:
        scraper.close()
        logging.info("Scraper fermé")

if __name__ == "__main__":
    print("Démarrage du scraping de Vinatis...")
    df = scrape_all_products(n_pages=2)
    
    # Sauvegarde finale
    if not df.empty:
        df.to_csv("vinatis_all_products.csv", index=False)
        print(f"\nScraping terminé. {len(df)} produits trouvés. Données enregistrées dans vinatis_all_products.csv")
    else:
        print("\nAucun produit trouvé. Le fichier n'a pas été créé.")

def accept_cookies(driver):
    try:
        # Essayez de trouver un bouton avec un texte courant pour accepter les cookies
        # Adaptez le sélecteur si besoin selon le HTML réel du bandeau
        buttons = driver.find_elements("xpath", "//button")
        for btn in buttons:
            txt = btn.text.strip().lower()
            if "accepter" in txt or "tout accepter" in txt or "j'accepte" in txt:
                btn.click()
                print("Bandeau cookies accepté.")
                time.sleep(1)
                break
    except Exception as e:
        print(f"Pas de bandeau cookies détecté ou erreur : {e}") 