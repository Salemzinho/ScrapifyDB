import re
import json

def validate_data(listing_data):
        
    listing_data['descricao'] = re.sub(r'&(lt|gt|amp|quot|apos|nbsp|copy|reg|#\d+);', '', listing_data['descricao'])
    listing_data['descricao'] = re.sub(r'<br\s*\/?>', '', listing_data['descricao'])
    listing_data['descricao'] = listing_data['descricao'].replace('&lt;', '').replace('&gt;', '').replace('&amp;', '').replace('&quot;', '').replace('&apos;', '').replace('&nbsp;', '').replace('&copy;', '').replace('&reg;', '').replace('&lt;br&gt;', '')

    #DEBUG
    #listing_data_formatted = json.dumps(listing_data, indent=4)
    #print(f"{listing_data_formatted}")
    #exit()
    
    return listing_data