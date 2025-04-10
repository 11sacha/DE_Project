from pyflink.datastream import StreamExecutionEnvironment
from pyflink.table import StreamTableEnvironment, EnvironmentSettings


env = StreamExecutionEnvironment.get_execution_environment()
settings = EnvironmentSettings.in_streaming_mode()
table_env = StreamTableEnvironment.create(env, environment_settings=settings)


KAFKA_BROKER = 'kafka:29092'

# Tabla de ad_impressions
table_env.execute_sql(f"""
    CREATE TABLE ad_impressions (
        impression_id STRING,
        user_id STRING,
        campaign_id STRING,
        ad_id STRING,
        device_type STRING,
        browser STRING,
        event_timestamp BIGINT,
        cost DOUBLE,
        event_time AS TO_TIMESTAMP_LTZ(event_timestamp, 3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'ad_impressions',
        'properties.bootstrap.servers' = '{KAFKA_BROKER}',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
""")

# Tabla de ad_clicks
table_env.execute_sql(f"""
    CREATE TABLE ad_clicks (
        click_id STRING,
        impression_id STRING,
        user_id STRING,
        event_timestamp BIGINT,
        event_time AS TO_TIMESTAMP_LTZ(event_timestamp, 3),
        WATERMARK FOR event_time AS event_time - INTERVAL '5' SECOND
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'ad_clicks',
        'properties.bootstrap.servers' = '{KAFKA_BROKER}',
        'format' = 'json',
        'scan.startup.mode' = 'earliest-offset'
    )
""")

# Tabla de salida: analytics_results
table_env.execute_sql(f"""
    CREATE TABLE analytics_results (
        window_start TIMESTAMP_LTZ(3),
        window_end TIMESTAMP_LTZ(3),
        campaign_id STRING,
        impressions BIGINT,
        clicks BIGINT,
        ctr DOUBLE
    ) WITH (
        'connector' = 'kafka',
        'topic' = 'analytics_results',
        'properties.bootstrap.servers' = '{KAFKA_BROKER}',
        'format' = 'json'
    )
""")

# Job: join + ventana de 1 minuto + cálculo de CTR
table_env.execute_sql("""
    INSERT INTO analytics_results
    SELECT
        TUMBLE_START(i.event_time, INTERVAL '1' MINUTE) AS window_start,
        TUMBLE_END(i.event_time, INTERVAL '1' MINUTE) AS window_end,
        i.campaign_id,
        COUNT(i.impression_id) AS impressions,
        COUNT(c.click_id) AS clicks,
        COUNT(c.click_id) * 1.0 / COUNT(i.impression_id) AS ctr
    FROM ad_impressions i
    LEFT JOIN ad_clicks c
    ON i.impression_id = c.impression_id
    AND c.event_time BETWEEN i.event_time AND i.event_time + INTERVAL '1' MINUTE
    GROUP BY TUMBLE(i.event_time, INTERVAL '1' MINUTE), i.campaign_id
""")
