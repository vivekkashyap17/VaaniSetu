class AnalyticsManager:


    total_requests = 0

    cache_hits = 0

    total_latency = 0.0

    language_requests = {}


    @classmethod
    def record_request(
        cls,
        language: str,
        latency: float,
        cache_hit: bool
    ):

        cls.total_requests += 1

        cls.total_latency += latency


        if cache_hit:

            cls.cache_hits += 1


        if language not in cls.language_requests:

            cls.language_requests[language] = 0


        cls.language_requests[language] += 1


    @classmethod
    def get_metrics(cls):

        average_latency = 0.0


        if cls.total_requests > 0:

            average_latency = (
                cls.total_latency / cls.total_requests
            )


        cache_hit_rate = 0.0


        if cls.total_requests > 0:

            cache_hit_rate = (
                cls.cache_hits / cls.total_requests
            ) * 100


        return {

            "total_requests": cls.total_requests,

            "cache_hits": cls.cache_hits,

            "cache_hit_rate": round(cache_hit_rate, 2),

            "average_latency": round(average_latency, 4),

            "language_requests": cls.language_requests
        }