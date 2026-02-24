from uuid import uuid4
from os import urandom
from hashlib import md5
from requests import Session

class ChessRoyale:
	def __init__(self, locale: str = "en") -> None:
		self.api = "https://master.chessroyale.app/api/v1"
		self.second_api = "https://api-v1-master.chessroyale.app"
		self.news_api = "https://api-news.whitesharx.app/starfall"
		self.session = Session()
		self.session.headers = {
			"user-agent": "UnityPlayer/2021.3.45f2 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
			"x-app-id": "com.xten.starfall",
			"x-app-version": "0.63.0+build.1586",
			"x-unity-version": "2021.3.45f2"
		}
		self.locale = locale
		self.player_id = None
		self.auth_token = None
		self.friend_code = None
		self.idfa = f"{uuid4()}"
		self.idfv = md5(urandom(15)).hexdigest()

	def login_as_guest(self) -> dict:
		data = {
			"locale": self.locale,
			"idfa": self.idfa,
			"idfv": self.idfv
		}
		response = self.session.post(
			f"{self.api}/auth/guest", json=data).json()
		if "token" in response:
			self.auth_token = response["token"]
			self.player_id = response["player"]["id"]
			self.friend_code = response["player"]["code"]
			self.session.headers["authorization"] = self.auth_token
		return response

	def login_with_auth_token(self, auth_token: str) -> dict:
		self.auth_token = auth_token
		self.session.headers["authorization"] = f"Bearer {self.auth_token}"
		response = self.get_current_player()
		if "player" in response:
			self.player_id = response["player"]["id"]
			self.friend_code = response["player"]["code"]
		return response

	def check_version(self, version: str) -> dict:
		return self.session.get(
			f"{self.api}/util/version/check?version={version}").json()

	def get_settings(self) -> dict:
		return self.session.get(F"{self.api}/settings").json()

	def get_current_player(self) -> dict:
		return self.session.get(f"{self.api}/players/me").json()

	def get_current_time(self) -> dict:
		return self.session.get(
			f"{self.api}/util/time/current").json()

	def get_current_olympiads(self) -> dict:
		return self.session.get(
			f"{self.api}/olympiads/current").json()


	def get_previous_olympiads(self) -> dict:
		return self.session.get(
			f"{self.api}/olympiads/previous").json()

	def get_clubs_list(self) -> dict:
		return self.session.get(
			f"{self.api}/clubs").json()

	def get_current_daily_mission(self) -> dict:
		return self.session.get(
			f"{self.api}/daily_missions/current").json()

	def get_plays_list(
			self,
			is_finished: bool = True,
			count: int = 10) -> dict:
		return self.session.get(
			f"{self.api}/plays?isFinished={is_finished}&count={count}").json()

	def get_current_rivals(self) -> dict:
		return self.session.get(
			f"{self.api}/rivals/current").json()

	def get_player_info(self, player_id: str) -> dict:
		return self.session.get(
			f"{self.api}/players/{player_id}").json()

	def get_player_achievements(self, player_id: str) -> dict:
		return self.session.get(
			f"{self.api}/simple_achievements/{player_id}").json()

	def get_leaderboard(
			self,
			type: str = "world",
			path: str = "clubPoints") -> dict:
		return self.session.get(
			f"{self.api}/leaderboard/{type}?path={path}").json()

	def get_storm_leaderboard(self) -> dict:
		return self.session.get(
			f"{self.api}/storm/leaderboard/count").json()

	def get_today_storm_leaderboard(self) -> dict:
		return self.session.get(
			f"{self.api}/storm/leaderboard/count/today").json()

	def get_series_storm_leaderboard(self) -> dict:
		return self.session.get(
			f"{self.api}/storm/leaderboard/count/series").json()

	def get_puzzles_leaderboard(self, type: str = "world") -> dict:
		return self.session.get(
			f"{self.api}/puzzles/leaderboard/{type}").json()

	def get_achievements_list(self) -> dict:
		return self.session.get(
			f"{self.second_api}/achievements").json()

	def change_flag(self, flag_icon: int) -> dict:
		data = {
			"flagIcon": flag_icon
		}
		return self.session.put(
			f"{self.api}/players/me/flag",
			json=data).json()

	def change_nickname(self, nickname: str) -> dict:
		data = {
			"nickname": nickname
		}
		return self.session.put(
			f"{self.api}/players/me/nickname", json=data).json()

	def get_news_list(self) -> dict:
		return self.session.get(
			f"{self.news_api}/{self.locale}/articles").json()

	def get_coin_reward(self, reward_number: int) -> dict:
		return requests.patch(
			f"{self.second_api}/rewarded/watch/{reward_number}").json()

	def spin_wheel(self) -> dict:
		return self.session.get(
			f"{self.api}/wheel/ad/twist").json()

	def get_shop(self) -> dict:
		return self.session.get(f"{self.api}/shop").json()
			
	def get_shop_coins(self) -> dict:
		return self.session.get(f"{self.api}/shop/coins").json()
			
	def get_shop_hints(self) -> dict:
		return self.session.get(f"{self.api}/shop/hints").json()

	def get_shop_avatars(self) -> dict:
		return self.session.get(f"{self.api}/shop/avatars").json()
	
	def get_shop_phrases(self) -> dict:
		return self.session.get(
			f"{self.api}/shop/hints/phrases").json()
	
	def get_shop_emoticons(self) -> dict:
		return self.session.get(f"{self.api}/shop/emoticons").json()
	
	def get_shop_boosters(self) -> dict:
		return self.session.get(f"{self.api}/shop/boosters").json()
	
	def get_shop_boards(self) -> dict:
		return self.session.get(f"{self.api}/shop/boards").json()
	
	def get_shop_safes(self) -> dict:
		return self.session.get(f"{self.api}/shop/safes").json()
	
	def get_shop_passes(self) -> dict:
		return self.session.get(f"{self.api}/shop/passes").json()

	def buy_item(
			self, category: str, item_id: str) -> dict:
		return self.session.post(
			f"{self.api}/shop/{category}/{item_id}").json()

	def claim_achievement(
			self,
			type: str,
			degree: int) -> dict:
		data = {
			"type": type,
			"degree": degree
		}
		return self.session.post(
			f"{self.api}/simple_achievements", json=data).json()

	def change_image_url(self, image_url: str) -> dict:
		data = {
			"imageUrl": image_url
		}
		return self.session.put(
			f"{self.api}/players/me/image_url", json=data).json()

	def get_puzzles(
			self, start: int = 1, end: int = 95) -> dict:
		return self.session.get(
			f"{self.second_api}/puzzles/map?from={start}&to={end}").json()

	def solve_puzzle(
			self, map_id: int, data: dict):
		return self.session.post(
			f"{self.second_api}/puzzles/map/{map_id}?isHasSubscription=false",
			json=data).json()

	def solve_storm(
			self, best_series: int, resolved_count: int) -> dict:
		data = {
			"storm": {
				"resolvedCount": resolved_count,
				"bestSeries": best_series
			},
			"isHasSubscription": False
		}
		return self.session.post(
			f"{self.api}/storm",
			json=data).json()
