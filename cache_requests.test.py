from cached_requests import Path, requests, delete_cache_by_expiration, delete_cache_by_function
from cached_requests.session import CacheSession
from datetime import timedelta, datetime, timezone
# from email.utils import parsedate_to_datetime

# from cached_requests import CacheSession
# from cached_requests.cloudscraper import CloudScraper as CacheSession
# response = CacheSession(
#     cache_dir=(Path.from_basedir(__file__) @ '.temp').ensure_exists(),
#     overwrite_allow_redirects=None
# )
def main() -> None:
    response = requests.get("https://google.com")
    print(response.text)
    # response = requests.get("https://postman-echo.com/time/now")
    # dt_global = parsedate_to_datetime(response.text)
    # dt_local = datetime.now(tz=timezone.utc)
    # print("GLOBAL UTC Time:", dt_global)
    # print("LOCAL  UTC Time:", dt_local)
    # print('gap: ', dt_local - dt_global)
    

if __name__ == "__main__":
    with requests.configure(
        cache_dir=(
            Path.from_basedir(__file__) @ 
            '.temp'
        ).ensure_exists(),
    ):
        main()
        delete_cache_by_expiration(requests, ex=timedelta(minutes=1))