import webbrowser

class Video:
	def __init__(self, title, link):
		self.title = title
		self.link = link
		self.seen = False

	def open(self):
		webbrowser.open(self.link)
		self.seen = True

class Playlist:
	def __init__(self, name, description, rating, videos):
		self.name = name
		self.description = description
		self.rating = rating
		self.videos = videos

def read_video():
	title = input("Enter title: ") + "\n"
	link = input("Enter link: ") + "\n"
	video = Video(title, link)
	return video

def print_video(video):
	print("Video title: ", video.title, end="")
	print("Video link: ", video.link, end="")

def read_videos():
	videos = []
	total_video =  int(input("Enter how many videos: "))
	for i in range(total_video):
		print("--- Enter video ", i+1, " ---")
		vid = read_video()
		videos.append(vid)
	return videos

def print_videos(videos):
	print("-----------")
	for i in range(len(videos)):
		print("--- Video", i+1, "---")
		print_video(videos[i]) 

def write_video_txt(video, f):
		f.write(video.title )
		f.write(video.link )

def write_videos_txt(videos, f):
	total = len(videos)
	f.write(str(total) + "\n")
	for i in range(total):
		write_video_txt(videos[i], f)

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

def read_playlist():
	playlist_name = input("Enter playlist name: ") + "\n"
	playlist_description = input("Enter playlist description: ") + "\n"
	playlist_rating = str(select_in_range("Enter rating(1-5): ",1,5)) + "\n"
	playlist_videos = read_videos()
	playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_videos)
	return playlist

def	write_playlist_txt(playlist):
	with open("data.txt", "w") as f:
		f.write(playlist.name)
		f.write(playlist.description)
		f.write(str(playlist.rating))
		write_videos_txt(playlist.videos, f)
	print("Goodbye!!!")

def read_playlist_from_txt():
	with open("data.txt", "r") as f:
		playlist_name = f.readline()
		playlist_description = f.readline()
		playlist_rating = f.readline()
		playlist_videos = read_videos_from_txt(f)
		playlist = Playlist(playlist_name, playlist_description, playlist_rating, playlist_videos)
	return playlist

def print_playlist(playlist):
	print("-----------")
	print("Playlist name: " + playlist.name, end = "")
	print("Playlist description: " + playlist.description, end = "")
	print("Playlist rating: ", playlist.rating, end = "")
	print_videos(playlist.videos)

def show_menu():
	print("Main Menu: ")
	print("-----------------------------")
	print("| Option 1: Create playlist |")
	print("| Option 2: Show playlist   |")
	print("| Option 3: Play a video    |")
	print("| Option 4: Add a video     |")
	print("| Option 5: Update playlist |")
	print("| Option 6: Remove a video  |")
	print("| Option 7: Find video      |")
	print("| Option 8: Save and Exit   |")
	print("-----------------------------")

def select_in_range(prompt, min, max):
	choice = input(prompt)
	while not choice.isdigit() or int(choice) < min or int(choice) > max :
		print("Wrong syntax! Enter again!")
		choice = input(prompt)
	choice = int(choice)
	return choice

def play_video(playlist):
	print_videos(playlist.videos)
	total = len(playlist.videos)
	choice = select_in_range("Select a video(1, " + str(total) + "): ", 1, total)
	print("Open video: " + playlist.videos[choice - 1].title + "Url: " + playlist.videos[choice - 1].link, end = "")
	playlist.videos[choice-1].open()

def add_video(playlist):	
	print("--- Enter new video information ---")
	new_video_title = input("Enter new video title: ") + "\n"
	new_video_link = input("Enter new video url: ")	+ "\n"
	new_video = Video(new_video_title, new_video_link)
	playlist.videos.append(new_video)
	return playlist

def update_playlist(playlist):
	print("--- Update playlist ---")
	print("1. Name")
	print("2. Description")
	print("3. Rating")
	choice = select_in_range("Enter what you want to update (1-3): ", 1, 3)
	if choice == 1:
		new_playlist_name = input("Enter new name for playlist: ") +"\n"
		playlist.name = new_playlist_name
		print("--- Updated Successfully!!! ---")
		return playlist
	if choice == 2:
		new_playlist_description = input("Enter new description for playlist: ") + "\n"
		playlist.description = new_playlist_description
		print("--- Updated Successfully!!! ---")
		return playlist
	if choice == 3:
		new_playlist_rating = str(select_in_range("Enter new rating for playlist (1-5): ", 1, 5)) + "\n"
		playlist.rating = new_playlist_rating
		print("--- Updated Successfully!!! ---")
		return playlist

def remove_video(playlist):
	print("--- Remove video ---")
	print_videos(playlist.videos)
	total = len(playlist.videos)
	choice = select_in_range("Enter video you want to delete: ", 1, total)
	del playlist.videos[choice - 1]

	'''
	new_video_list = []
	for i in range(total):
		if i == choice -1:
			continue
		new_video_list.append(playlist.video[i])
	playlist.videos = new_video_list
	'''

	return playlist

def find_video(playlist):
	print("--- Find video ---")
	find_vid = input("Enter the video name: ") + "\n"
	for i in range(len(playlist.videos)):
		if find_vid == playlist.videos[i].title:
			print("--- Bingo ---")
			print("Open video: " + playlist.videos[i].title + "Url: " + playlist.videos[i].link, end = "")
			playlist.videos[i].open()
			find_vid = True
	if find_vid != True:
		print("Sorry your video is not in playlist", playlist.name)


def main():
	try:
		playlist = read_playlist_from_txt()
		print("Loaded Data successfully!")

	except:
		print("Welcome first user!! ")

	while True:
		show_menu()
		choice = select_in_range("Select an option (1-8): ", 1, 8)
		if choice == 1:
			playlist = read_playlist()
			input("\n--- Press Enter to continue. --- \n")
		if choice == 2:
			print_playlist(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 3:
			play_video(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 4:
			playlist = add_video(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 5:
			playlist = update_playlist(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 6:
			playlist = remove_video(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 7:
			find_video(playlist)
			input("\n--- Press Enter to continue. --- \n")
		if choice == 8:
			write_playlist_txt(playlist)
			break

main()