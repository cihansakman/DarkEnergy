from cloud_metric_collector import MetricDataCollector

collector = MetricDataCollector('../cloud_credentials.json')

#Report last 7 days
time_interval_minutes = 7 * 24 * 60

#Call the function
collector.collect_metric_data(time_interval_minutes)


from cloud_power_consumption_calculator import MetricAnalyzer
analyzer = MetricAnalyzer('../metric_data.csv', DISKSPACE=10, MEMORY=2, compute_processor='BROADWELL', region='EUROPE-WEST6')
metric_data = analyzer.load_metric_data()
analyzer.plot_metrics(metric_data)