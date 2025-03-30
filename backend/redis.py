import pickle
import zlib
import pandas as pd

def fetch_data_from_redis_or_mongodb(stock_symbol, redis, mongo_db):
    try:
        cached_data = redis.get(stock_symbol)
        if cached_data:
            df = pickle.loads(zlib.decompress(cached_data))
            return df
        else:
            collection = mongo_db[stock_symbol]
            cursor = collection.find()
            df = pd.DataFrame(list(cursor))
            if not df.empty:
                compressed_df = zlib.compress(pickle.dumps(df))
                redis.setex(stock_symbol, 60, compressed_df)
            return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return pd.DataFrame()
