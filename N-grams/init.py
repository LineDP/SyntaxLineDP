
data_path="/data/zhujz/linedp/Datasets/preprocessed_data3/"
projects=['activemq','camel','derby','groovy','hbase','hive','jruby','lucene','wicket']
all_releases = {'activemq': ['activemq-5.0.0', 'activemq-5.1.0', 'activemq-5.2.0', 'activemq-5.3.0', 'activemq-5.8.0'],
                'camel': ['camel-1.4.0', 'camel-2.9.0', 'camel-2.10.0', 'camel-2.11.0'],
                'derby': ['derby-10.2.1.6', 'derby-10.3.1.4', 'derby-10.5.1.1'],
                'groovy': ['groovy-1_5_7', 'groovy-1_6_BETA_1', 'groovy-1_6_BETA_2'],
                'hbase': ['hbase-0.94.0', 'hbase-0.95.0', 'hbase-0.95.2'],
                'hive': ['hive-0.9.0', 'hive-0.10.0', 'hive-0.12.0'],
                'jruby': ['jruby-1.1', 'jruby-1.4.0', 'jruby-1.5.0', 'jruby-1.7.0.preview1'],
                'lucene': ['lucene-2.3.0', 'lucene-2.9.0', 'lucene-3.0.0', 'lucene-3.1'],
                'wicket': ['wicket-1.3.0-incubating-beta-1', 'wicket-1.3.0-beta2', 'wicket-1.5.3']}

def myreplace(matched):
    return " " + matched.group(0) + " "