from requests import get
import threading

class GetPlatform(object):
    
    def __init__(self,data):

        self.results = data['results']
        
       
        
    def getRentingPlatform(self):

        try:
            rent = self.results['ES']['rent']
            renting_list = []

            for index in range(len(rent)):

                dicta = {'provider_name': rent[index]['provider_name'],
                        'logo_path': rent[index]['logo_path'],
                        }
                renting_list.append(dicta)

            return renting_list
        except KeyError as ke:
                
            if str(ke) == 'rent':
                pass 
            else:
                pass
        
  
        
    
    def getBuyingPlatform(self):

        try:
            buy = self.results['ES']['buy']
            buying_list = []
            
            for index in range(len(buy)):
                dicta = {'provider_name': buy[index]['provider_name'],
                        'logo_path': buy[index]['logo_path'],
                        }
                buying_list.append(dicta)

            return buying_list
        
        except KeyError as ke:
                
            if str(ke) == 'buy':
                pass 
            else:
                pass

    def getStreamingPlatform(self):

        try:
            stream = self.results['ES']['flatrate']
            streaming_list = []
            
            for index in range(len(stream)):
                dicta = {'provider_name': stream[index]['provider_name'],
                        'logo_path': stream[index]['logo_path'],
                        }
                streaming_list.append(dicta)

            return streaming_list
        
        except KeyError as ke:
                
            if str(ke) == 'flatrate':
                pass 
            else:
                pass




class Movie():
    def __init__(self,movie_info):
        
        self.id = movie_info['id']
        self.name = movie_info['title']
        self.release_date = movie_info['release_date']
        self.backdrop_path = movie_info['backdrop_path']
    
        



def getMovieID(query):

    url_busqueda = "https://api.themoviedb.org/3/search/movie"
    api_key = 'c46ea27b682c7ee36802a793a2db70d8'
    params = {
        'api_key': api_key,
        'language':'es-ES',
        'query': query,
    }

    response = get(url_busqueda,params)
   
    response = response.json()
    data = response['results']
    movies = []
    for movie_info in data:

        movie_info = Movie(movie_info)
        id = movie_info.id
        name = movie_info.name
        release_date = movie_info.release_date
        backdrop_path = movie_info.backdrop_path
        
        movies.append({'id': id,
                       'title': name,
                       'release_date': release_date,
                       'backdrop_path': backdrop_path,
                    })

    return movies    


def getResponse(movie_id):

    api_key = 'c46ea27b682c7ee36802a793a2db70d8'
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/watch/providers"
    params = {
        'api_key':api_key,
        'language': 'es-ES',
    }   
    response = get(url,params)

    return response.json()

def processMovie(movie_info, movies_list):
    try:
        movie = Movie(movie_info)
        transform_movies = GetPlatform(getResponse(movie.id))
        movies_dict = {
            'name': movie.name,
            'release_date':movie.release_date,
            'backdrop_path':movie.backdrop_path,
            'buy': transform_movies.getBuyingPlatform(),
            'rent': transform_movies.getRentingPlatform(),
            'flatrate':transform_movies.getStreamingPlatform(),
        }
        movies_list.append(movies_dict)
    except Exception as e:
        print(f'Ha habido un error: {e}')



def getInfoWithThreading(movies):

    

    movies_list = []
    threads = []

    for movie_info in movies:
        thread = threading.Thread(target=processMovie, args=(movie_info, movies_list))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return movies_list


