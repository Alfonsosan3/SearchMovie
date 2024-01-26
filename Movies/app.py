from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.uix.image import AsyncImage
from kivy.core.window import Window
from kivy.uix.widget import Widget


from index import getInfoWithThreading,getMovieID

class SearchScreen(Screen):
    def __init__(self, **kwargs):

        super(SearchScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='horizontal',size_hint_y=None,pos_hint = {'center_x': 0.5, 'center_y': 0.5},height = 40)
        self.search_input = TextInput(font_size=55,
            multiline=False,
            size_hint=(0.8, None),  # Ajusta el valor según tus necesidades
            pos_hint={'center_x': 0.5, 'center_y': 0},
            halign='center')
        
        search_button = Button(on_press=self.switchToMovies,
            text= 'Buscar',
            size_hint=(0.4, None),
            pos_hint={'center_x': 0.5, 'center_y': 0}  # Ajusta el valor según tus necesidades
            )

        layout.add_widget(self.search_input)
        layout.add_widget(search_button)

        self.add_widget(layout)
    
    def switchToMovies(self, instance):

        query = self.search_input.text
        movie_ids = getMovieID(query)
        movies_list = getInfoWithThreading(movie_ids)

        
        movies_screen = self.manager.get_screen('movies')
        movies_screen.update_movies(movies_list)

        self.manager.current = 'movies'

class MoviesScreen(Screen):

    def __init__(self, **kwargs):
        super(MoviesScreen, self).__init__(**kwargs)

        layout = BoxLayout(orientation='vertical')
        

        
        self.movies_scrollview = ScrollView(size_hint=(0, None), size=(Window.width, Window.height))
        self.movies_label = BoxLayout(orientation='vertical', size_hint_y=None)

        
        self.movies_scrollview.add_widget(self.movies_label)
        layout.add_widget(self.movies_scrollview)

        self.add_widget(layout)

    

    def update_movies(self, movies_list):
        self.movies_label.clear_widgets()

        for movie in movies_list:

            movie_box = BoxLayout(orientation = 'horizontal',padding =(10,0,10,0) )
            image_text_box = BoxLayout(orientation = 'vertical')
            buy_box = BoxLayout(orientation = 'horizontal')
            rent_box = BoxLayout(orientation = 'horizontal')
            stream_box = BoxLayout(orientation = 'horizontal')
            platform_box = BoxLayout(orientation= 'vertical',padding =(0,75,0,0)) #top: 100 no esta nada mal
            

            
            if len(movie['name']) >= 32:

                movie['name'] = movie['name'][:29] + "..."

            image_text_box.add_widget(Label(text=f"{movie['name']}\n{movie['release_date']}",font_size=16))
            
            if 'backdrop_path' in movie:

                async_image = (AsyncImage(source = f"https://image.tmdb.org/t/p/original/{movie['backdrop_path']}", size_hint = (1, None), size=(150,150)))
                
                image_text_box.add_widget(async_image)

            movie_box.add_widget(image_text_box)
            
            
            try:

                

                if movie['buy'] is not None:
                    buy_box.add_widget(Label(text = 'Comprar:',size_hint=(None, 1)))
                    for logo in movie['buy']:
                        buy_box.add_widget(AsyncImage(source = f"https://image.tmdb.org/t/p/original/{logo['logo_path']}", size_hint=(None, 1), keep_ratio=False,size=(40,40)))

                else:
                    buy_box.add_widget(Label(text = 'Comprar:       ',size_hint=(None, 1)))
                    buy_box.add_widget(Label(text = 'No disponible en España',size_hint=(None, 1)))    
                
                    

                if movie['rent'] is not None:
                    rent_box.add_widget(Label(text = 'Alquilar:',size_hint=(None, 1)))
                    for logo in movie['rent']:
                        rent_box.add_widget(AsyncImage(source = f"https://image.tmdb.org/t/p/original/{logo['logo_path']}", size_hint=(None, 1), keep_ratio=False,size=(40,40)))    
                else:
                    rent_box.add_widget(Label(text = 'Alquilar:       ',size_hint=(None, 1)))
                    rent_box.add_widget(Label(text = 'No disponible en España',size_hint=(None, 1))) 
                    
                
                

                if movie['flatrate'] is not None:
                    stream_box.add_widget(Label(text = 'Stream:',size_hint=(None, 1)))
                    for logo in movie['flatrate']:
                    
                        stream_box.add_widget(AsyncImage(source = f"https://image.tmdb.org/t/p/original/{logo['logo_path']}", size_hint=(None, 1), keep_ratio=False,size=(40,40)))
                else:
                    stream_box.add_widget(Label(text = 'Stream:      ',size_hint=(None, 1)))
                    stream_box.add_widget(Label(text = 'No disponible en España',size_hint=(None, 1)))
            except:
                pass
                


            platform_box.add_widget(buy_box)
            platform_box.add_widget(rent_box)
            platform_box.add_widget(stream_box)


            

            movie_box.add_widget(platform_box)

            separator_line = Widget(size_hint_y=None, height=2)
            
            
            self.movies_label.add_widget(movie_box)
            self.movies_label.add_widget(separator_line)

        
        self.movies_label.height = len(movies_list) * 250




    



class MovieApp(App):
    
    def build(self):
        screen_manager = ScreenManager()
        
        search_screen = SearchScreen(name='search')
        movies_screen = MoviesScreen(name='movies')

        screen_manager.add_widget(search_screen)
        screen_manager.add_widget(movies_screen)
        
        return screen_manager















if __name__ == '__main__':
    MovieApp().run()