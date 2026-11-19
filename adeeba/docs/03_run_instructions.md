# Run Instructions

## Local test (Hadoop ke bina) - Anaconda Prompt (CMD)
Job 1 quality:  type ..\..\sample-data\sample.csv | python mapper.py | sort | python reducer.py
Job 1 clean:    type ..\..\sample-data\sample.csv | python clean_mapper.py | sort | python clean_reducer.py
Job 2:          type ..\..\sample-data\clean_out.csv | python mapper.py | sort | python combiner.py | sort | python reducer.py
Job 3 pass A:   type ..\..\sample-data\sample_anomaly.csv | python mapper_a.py | sort | python reducer_a.py > ..\..\sample-data\statsA_out.txt
Job 3 pass B:   (type ..\..\sample-data\sample_anomaly.csv | python mapper_b.py & type ..\..\sample-data\statsA_out.txt | python mapper_b.py) | sort | python reducer_b.py
Job 4:          type ..\..\sample-data\clean_out.csv | python mapper.py | sort | python reducer.py

Expected outputs: adeeba\sample-data\expected_*.

## Hadoop par chalana
Hadoop install aur HDFS folders Eshal ke setup ke baad. Commands us waqt yahan add honge.

## Naya streaming data aane par
Naya data /climate/raw/streaming/ mein aata hai. Jobs dobara chalao (Job 1 clean -> Job 2, 3, 4),
phir Impala mein REFRESH <table>; chalao.