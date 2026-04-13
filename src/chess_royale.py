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
			"User-Agent": "UnityPlayer/2021.3.45f2 (UnityWebRequest/1.0, libcurl/8.5.0-DEV)",
			"X-App-Id": "com.xten.starfall",
			"X-App-Version": "0.63.0+build.1586",
			"X-Unity-Version": "2021.3.45f2"
		}
		self.locale = locale
		self.player_id = None
		self.auth_token = None
		self.friend_code = None
		self.idfa = f"{uuid4()}"
		self.idfv = md5(urandom(15)).hexdigest()

	def _get(self, endpoint: str, params: dict = {}) -> dict:
		return self.session.get(endpoint, params=params).json()

	def _post(self, endpoint: str, data: dict = None) -> dict:
		return self.session.post(endpoint, json=data).json()

	def _put(self, endpoint: str, data: dict = None) -> dict:
		return self.session.put(endpoint, json=data).json()

	def login_as_guest(self) -> dict:
		data = {
			"locale": self.locale,
			"idfa": self.idfa,
			"idfv": self.idfv
		}
		response = self._post(f"{self.api}/auth/guest", data)
		if "token" in response:
			self.auth_token = response["token"]
			self.player_id = response["player"]["id"]
			self.friend_code = response["player"]["code"]
			self.session.headers["authorization"] = self.auth_token
		return response

	def login_with_auth_token(self, auth_token: str) -> dict:
		self.auth_token = auth_token
		self.session.headers["Authorization"] = f"Bearer {self.auth_token}"
		response = self.get_current_player()
		if "player" in response:
			self.player_id = response["player"]["id"]
			self.friend_code = response["player"]["code"]
		return response

	def get_settings(self) -> dict:
		return self._get(f"{self.api}/settings")

	def get_current_player(self) -> dict:
		return self._get(f"{self.api}/players/me")

	def get_current_time(self) -> dict:
		return self._get(
			f"{self.api}/util/time/current")

	def get_current_olympiads(self) -> dict:
		return self._get(
			f"{self.api}/olympiads/current")

	def get_previous_olympiads(self) -> dict:
		return self._get(
			f"{self.api}/olympiads/previous")

	def get_clubs_list(self) -> dict:
		return self._get(
			f"{self.api}/clubs")

	def get_current_daily_mission(self) -> dict:
		return self._get(
			f"{self.api}/daily_missions/current")

	def get_plays_list(
			self,
			is_finished: bool = True,
			count: int = 10) -> dict:
		params = {
			"isFinished": is_finished,
			"count": count
		}
		return self._get(f"{self.api}/plays", params)

	def get_current_rivals(self) -> dict:
		return self._get(
			f"{self.api}/rivals/current")

	def get_player_info(self, player_id: str) -> dict:
		return self._get(
			f"{self.api}/players/{player_id}")

	def get_player_achievements(self, player_id: str) -> dict:
		return self._get(
			f"{self.api}/simple_achievements/{player_id}")

	def get_leaderboard(
			self,
			type: str = "world",
			path: str = "clubPoints") -> dict:
		params = {
			"path": path
		}
		return self._get(
			f"{self.api}/leaderboard/{type}", params)

	def get_storm_leaderboard(self) -> dict:
		return self._get(
			f"{self.api}/storm/leaderboard/count")

	def get_today_storm_leaderboard(self) -> dict:
		return self._get(
			f"{self.api}/storm/leaderboard/count/today")

	def get_series_storm_leaderboard(self) -> dict:
		return self._get(
			f"{self.api}/storm/leaderboard/count/series")

	def get_puzzles_leaderboard(self, type: str = "world") -> dict:
		return self._get(
			f"{self.api}/puzzles/leaderboard/{type}")

	def get_achievements_list(self) -> dict:
		return self._get(f"{self.second_api}/achievements")

	def change_flag(self, flag_icon: int) -> dict:
		data = {
			"flagIcon": flag_icon
		}
		return self._put(
			f"{self.api}/players/me/flag", data)

	def change_nickname(self, nickname: str) -> dict:
		data = {
			"nickname": nickname
		}
		return self._put(
			f"{self.api}/players/me/nickname", data)

	def get_news_list(self) -> dict:
		return self._get(
			f"{self.news_api}/{self.locale}/articles")

	def get_coin_reward(self, reward_number: int) -> dict:
		return self.session.patch(
			f"{self.second_api}/rewarded/watch/{reward_number}").json()

	def spin_wheel(self) -> dict:
		return self._get(f"{self.api}/wheel/ad/twist")

	def get_shop(self) -> dict:
		return self._get(f"{self.api}/shop")
			
	def get_shop_coins(self) -> dict:
		return self._get(f"{self.api}/shop/coins")
			
	def get_shop_hints(self) -> dict:
		return self._get(f"{self.api}/shop/hints")

	def get_shop_avatars(self) -> dict:
		return self._get(f"{self.api}/shop/avatars")
	
	def get_shop_phrases(self) -> dict:
		return self._get(
			f"{self.api}/shop/hints/phrases")
	
	def get_shop_emoticons(self) -> dict:
		return self._get(f"{self.api}/shop/emoticons")
	
	def get_shop_boosters(self) -> dict:
		return self._get(f"{self.api}/shop/boosters")
	
	def get_shop_boards(self) -> dict:
		return self._get(f"{self.api}/shop/boards")
	
	def get_shop_safes(self) -> dict:
		return self._get(f"{self.api}/shop/safes")
	
	def get_shop_passes(self) -> dict:
		return self._get(f"{self.api}/shop/passes")

	def buy_item(
			self, category: str, item_id: str) -> dict:
		return self._post(f"{self.api}/shop/{category}/{item_id}")

	def claim_achievement(
			self,
			type: str,
			degree: int) -> dict:
		data = {
			"type": type,
			"degree": degree
		}
		return self._post(f"{self.api}/simple_achievements", data)

	def change_image_url(self, image_url: str) -> dict:
		data = {
			"imageUrl": image_url
		}
		return self._put(
			f"{self.api}/players/me/image_url", data)

	def get_puzzles(
			self, start: int = 1, end: int = 95) -> dict:
		params = {
			"from": start,
			"to": end
		}
		return self._get(
			f"{self.second_api}/puzzles/map", params)

	def solve_puzzle(
			self, map_id: int, data: dict):
		return self._post(
			f"{self.second_api}/puzzles/map/{map_id}?isHasSubscription=false", data)

	def solve_storm(
			self, best_series: int, resolved_count: int) -> dict:
		data = {
			"storm": {
				"resolvedCount": resolved_count,
				"bestSeries": best_series
			},
			"isHasSubscription": False
		}
		return self._post(f"{self.api}/storm", data)
