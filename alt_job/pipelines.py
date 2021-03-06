# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class AddKeywordMatchesPipeline(object):
    
    # English and French keywords
    matches=list(set([   

        "climate", "animal", "wildlife", "biomass", "pollution", "conservation", "biodiversity", 
        "nature", "ecotourism", "sustainable", "renewable", "energy", "environment", "education", "food",
        "agriculture", "organic", "farming", "forest", "green", "social",  "business", "entrepreneurship", 
        "leadership", "media", "journalism", "food security", "health", "ocean", "bike", "recycle", "waste",
        "intership"
        
        "climat", "animal", "faune", "biomasse", "pollution", "conservation", "biodiversité", 
        "nature", "écotourisme", "durable", "renouvelable", "énergie", "environnement", "éducation", "alimentation",
        "agriculture", "biologique", "agriculture", "forêt", "vert", "social", "entreprise", "esprit d'entreprise", 
        "leadership", "médias", "journalisme", "sécurité alimentaire", "santé", "océan", "vélo", "recyclage", "déchets",
        "stage"

    ]))
    
    def process_item(self, item, spider):
        
        item['keywords_matched'] = [m for m in self.matches if m in item.get_text()]
        
        return item

    # TODO explore ways to use natural language processing to dig out most relevent keywords
    #   https://github.com/danielgulloa/jobMatch
    #   https://github.com/2dubs/Job-Skills-Extraction
