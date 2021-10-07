import pymongo
 
#conexão com o mongo
#[retorno é uma referencia para o BD]
def connection(name_bd):
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient[name_bd]
    return mydb

#buscar uma collection especifica informando o nome da collection e do banco
#[retorno é um dicionário com a collection]
def get_collection(name_collection, mydb):
    collection = mydb[name_collection]
    return collection

#buscar se há um arquivo com tema presente em uma collection informando nome da collection e tema
#[retorno é um dicionário do arquivo caso exista ou
# None se não houver o tema na collection]
def search_theme(theme, collection):
    return collection.find_one({"tema":theme})

#verifica se o id do tweet já existe no documento da collection
#new id é o id do tweet a ser salvo e collection deve ser um dicionário do arquivo que foi
# obtido com search_theme
#[retorno true caso id já existe ou
# falso caso não exista]
def exist_id(new_id, collection):
    for item in collection.get('tweet'):
        if(item.get('id_tweet')==new_id):
            return True
    
    return False

#verifica em todas as collections se tweet já existe na base de dados
#recebe como parametro o nome de todas as collections do BD, nome do banco, nome do tema
#  e id do tweet respectivamente
#[retorna True se já existir na base e False caso não exista]
def exist_tweet(all_NamesCollections, mydb, theme, id_tt):
    #buscar em cada collection se há o tema do tweet
    #a variável s vai controlar a posição de cada collection
    s=0
    while(s<len(all_NamesCollections)):
        atual_collection = get_collection(all_NamesCollections[s],mydb)
        dict_collection  = search_theme(theme,atual_collection)

        #se for um tema novo (dict_collection recebeu um None)
        #vamos dar append para salvar depois
        if(dict_collection==None):
            return False
                
        #caso o tema exista é necessário verificar se já existe no BD
        else:
            #varrer todos os tweets
            #se exist_id retornar True, esse tweet já está presente na base de dados
            if(exist_id(id_tt,dict_collection)):
                return True
            else:
                s=s+1

    #se a varredura passou por todas as collections sem problemas, é um tweet a ser salvo
    if(s==len(all_NamesCollections)):
         return False
    else:
        return True

#retorna uma lista de dicionarios
#cada dicionario tem a forma {'tema':'nome_tema', 'tweets': []}
#em tweets sera uma lista de tweets sobre cada tema presente na collection

#recebe como parametro uma collection
def get_all_tweets(collection):
    l_tweets=[]
    for doc in collection.find():    
        j=0 #controla cada tema da collection

        i=0 #controla cada tweet sobre o tema

        #criar o dicionario para o tema
        dic={'tema':doc['tema'],'tweets':[]}
        while(i<len(doc['tweet'])):
            dic['tweets'].append(doc['tweet'][i]['texto'])
            i=i+1

        l_tweets.append(dic)
        j=j+1
    
    return l_tweets