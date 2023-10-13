import requests
import xml.etree.ElementTree as ET


def search_pubmed(key,nid):

  # PubMed API URL for searching
  base_search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"

  # PubMed API URL for fetching article details
  base_fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"

  # PubMed API key
  api_key = "48eb0384ae43d7a49e5a1d48a53debf2c109"

  # Construct parameters for the search request
  search_params = {
    "db": "pubmed",
    "term": key,
    "api_key": api_key,
    "retmax": nid}

  # Send the search request
  search_response = requests.get(base_search_url, params=search_params)

  if search_response.status_code == 200:
    # Parse the XML response to get a list of article IDs
    root = ET.fromstring(search_response.text)
    article_ids = [elem.text for elem in root.findall(".//Id")]
    
    # Create a list for the output
    pubmed_out=[]
    
    # Iterate through the article IDs and retrieve article details
    for article_id in article_ids:
      # Construct parameters for fetching article details
      fetch_params = {
        "db": "pubmed",
        "id": article_id,
        "api_key": api_key,
        "retmode": "xml"}
        
      # Send the fetch request
      fetch_response = requests.get(base_fetch_url, params=fetch_params)
        
      if fetch_response.status_code == 200:
        # Parse the XML response to extract article details
        article_root = ET.fromstring(fetch_response.text)
        article_title = article_root.find(".//ArticleTitle").text
        abstract_element = article_root.find(".//AbstractText")
        article_abstract = abstract_element.text if abstract_element is not None else "No abstract available."
            
        # Write the details in the list of results
        pubmed_out.append(f"{key}\t{article_id}\t{article_title}\t{article_abstract}\n")
      else:
        print("Failed to retrieve article with ID:", article_id)
    
    
  else:
    print("Search request failed with status code:", search_response.status_code)
  
  return pubmed_out



list_chem = ["[4-Chloro-6-(2,3-xylidino)-2-pyrimidinylthio]acetic acid",
"Acrylamide",
"Propofol",
"Caffeine",
"Chlorpyrifos",
"Chlorpyrifos oxon",
"Genistein",
"Niflumic acid",
"Pregnenolone",
"Dexamethasone",
"4,5-Dihydro-2-mercaptoimidazole",
"Diphenylamine",
"Valproic acid",
"(+/-)-Verapamil",
"Diclofenac",
"Bisphenol A",
"Clofibric acid",
"Carbendazim",
"2-Butoxyethanol",
"Tamoxifen",
"Cyclosporin A",
"Tetracycline",
"2-Aminophenol",
"Acetaminophen",
"2,4,4'-Trichlorobiphenyl",
"Atrazine",
"Paraquat",
"Amiodarone",
"Kepone",
"2-Ethylhexyl diphenyl phosphate"]




out_list=[]
for chem in list_chem:
  out_list.extend(search_pubmed(chem,5))
  

# exporting all in a tsv file to open with excel
tsv_file = open("pubmed_results.tsv", "w", encoding="utf-8")
for line in out_list:
  tsv_file.write(line)
tsv_file.close()







