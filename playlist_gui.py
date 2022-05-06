import pygame
import webbrowser
from urllib.request import urlopen
import io
from urllib.parse import urlparse, parse_qs


class Video:
    def __init__(self, title, link):
        self.title = title
        self.link = link
        self.seen = False

    def open(self):
        webbrowser.open(self.link)
        print("Open " + self.title)
        self.seen = True

class Playlist:
    def __init__(self, name, description, rating, image_url, videos):
        self.name = name
        self.description = description
        self.rating = rating
        self.image_url = image_url
        self.videos = videos

class TextButton:
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.seen = False

    def is_mouse_on_txt(self):
        self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
        if self.pos[0] < self.mouse_x < self.pos[0] + self.text_box[2] and self.pos[1] < self.mouse_y < self.pos[1] + self.text_box[3] :
            return True
        else:
            return False

    def draw(self, ill, image_url):
        self.illustration = ill
        self.image = image_url
        font = pygame.font.SysFont('Consolas', 20)
        text_render = font.render(self.text, True, WHITE)
        self.text_box = text_render.get_rect()
        margin = 12

        if self.is_mouse_on_txt():
            text_render = font.render(self.text, True, (0,0,255))
            pygame.draw.line(screen, (0,0,255), (self.pos[0],self.pos[1] + self.text_box[3]),(self.pos[0] + self.text_box[2], self.pos[1] + self.text_box[3]))

            font1 = pygame.font.SysFont('arial', 15)
            text_render1 = font1.render(self.illustration, True, (20,20,20))
            self.text_box1 = text_render1.get_rect()
            pygame.draw.rect (screen, (200,200,200),(self.mouse_x + margin,self.mouse_y + margin,self.text_box1[2],self.text_box1[3]))

            image_str = urlopen(image_url).read()
            image_file = io.BytesIO(image_str)
            image = pygame.image.load(image_file)
            img = pygame.transform.smoothscale(image, (350, 350))
            img_box = img.get_rect()
            img_box = img_box.move((50, 300))

            screen.blit(text_render1, (self.mouse_x + margin,self.mouse_y + margin))
            screen.blit(img, img_box)

        else:
            text_render = font.render(self.text, True, WHITE)
        
        if self.seen == True:
            text_render = font.render(self.text, True, (129, 16, 163))
            pygame.draw.line(screen, (129, 16, 163), (self.pos[0],self.pos[1] + self.text_box[3]),(self.pos[0] + self.text_box[2], self.pos[1] + self.text_box[3]))

        screen.blit(text_render, self.pos)


def read_video_from_txt(f):
    title = f.readline()
    link = f.readline()
    video = Video(title, link)
    return video

def read_videos_from_txt(f):
    videos = []
    total = f.readline()
    for i in range(int(total)):
        video = read_video_from_txt(f)
        videos.append(video)
    return videos

def read_playlist_from_txt(f):
    playlist_name = f.readline()
    playlist_description = f.readline()
    playlist_rating = f.readline()
    playlist_image_url = f.readline()
    playlist_videos = read_videos_from_txt(f)
    playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_image_url, playlist_videos)
    return playlist

def read_playlists_from_txt():
    playlists = []
    with open('data.txt', "r") as f:
        total = f.readline()
        for i in range(int(total)):
            playlist = read_playlist_from_txt(f)
            playlists.append(playlist)
            
    return playlists

pygame.init()
screen = pygame.display.set_mode((800, 650))
pygame.display.set_caption('Youtube Playlist')
running = True
WHITE = (255,255,255)
GREY = (50, 50, 70)
clock = pygame.time.Clock()

#Load data
playlists = read_playlists_from_txt()
playlists_btn_list = []
playlists_ill_list = []
playlists_img_list = []

margin = 50

for i in range(len(playlists)):
    playlist_btn = TextButton( str(i+1) + ". " + playlists[i].name.rstrip(), (50, 50 + margin*i))
    playlists_btn_list.append(playlist_btn)
    playlists_btn_list[i].illustration = "Description: " + playlists[i].description.rstrip()
    playlists_ill_list.append(playlists_btn_list[i].illustration)
    playlists_btn_list[i].image_url = playlists[i].image_url.rstrip()
    playlists_img_list.append(playlists_btn_list[i].image_url)

videos_btn_list = []
videos_ill_list = []
videos_img_list = []
choice = None

while running:		
    clock.tick(60)
    screen.fill(GREY)

    for i in range(len(playlists_btn_list)):
        playlists_btn_list[i].draw(playlists_ill_list[i], playlists_img_list[i])
    for i in range(len(videos_btn_list)):
        videos_btn_list[i].draw(videos_ill_list[i], videos_img_list[i])
        
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                for i in range(len(playlists_btn_list)):
                    if playlists_btn_list[i].is_mouse_on_txt():
                        choice = i
                        videos_btn_list = []
                        # urls_list = []
                        for j in range(len(playlists[i].videos)):
                            video_btn = TextButton( str(j+1) + ". " + playlists[i].videos[j].title.rstrip(), (300, 50 + margin*j))
                            videos_btn_list.append(video_btn)
                            videos_btn_list[j].illustration = "Url: " + playlists[i].videos[j].link.rstrip()
                            url_data = urlparse(playlists[i].videos[j].link.rstrip())
                            query = parse_qs(url_data.query)
                            video_id = query["v"][0]
                            videos_btn_list[j].image_url = "https://img.youtube.com/vi/" + video_id +"/maxresdefault.jpg"
                            videos_ill_list.append(videos_btn_list[j].illustration)
                            videos_img_list.append(videos_btn_list[j].image_url)
                if choice != None:
                    for i in range(len(videos_btn_list)):
                        if videos_btn_list[i].is_mouse_on_txt():
                            playlists[choice].videos[i].open()
                            videos_btn_list[i].seen = playlists[choice].videos[i].seen

        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()