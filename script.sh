apt-get -y update && apt-get -y upgrade
#install java
add-apt-repository ppa:webupd8team/java
apt-get -y upgrade && apt-get install oracle-java8-installer

#install elasticsearch
wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-6.4.1.deb
dpkg -i elasticsearch-6.4.1.deb

#configure elasticsearch
sed -i 's/#cluster.name: my-application/cluster.name: eastwatch/g' /etc/elasticsearch/elasticsearch.yml
sed -i 's/#network.host: 192.168.0.1/network.host: 0.0.0.0/g' /etc/elasticsearch/elasticsearch.yml
sed -i 's/#http.port: 9200/http.port: 9201/g' /etc/elasticsearch/elasticsearch.yml

#install kibana
wget https://artifacts.elastic.co/downloads/kibana/kibana-6.4.1-amd64.deb
dpkg -i kibana-6.4.1-amd64.deb

#configure kibana
sed -i 's/#server.name: "your-hostname"/"server.name: "eastwatch"/g' /etc/kibana/kibana.yml
sed -i 's/#server.host: "localhost""/"server.host: "0.0.0.0"/g' /etc/kibana/kibana.yml
sed -i 's=#elasticsearch.url: "http://localhost:9200"=elasticsearch.url: "http://localhost:9201"=g' /etc/kibana/kibana.yml

#install nginx
apt-get install nginx
#printf "kibana:$(openssl passwd -crypt pHwtF5)n" > /etc/nginx/htpassw_k
#printf "elastic:$(openssl passwd -crypt FpXXrkZ^*fv-tn5PVM$w)n" > /etc/nginx/htpassw_e
sh -c "echo -n 'kibana:' >> /etc/nginx/htpassw_k"
sh -c "openssl passwd pHwtF5 >> /etc/nginx/htpassw_k"
sh -c "echo -n 'elastic:' >> /etc/nginx/htpassw_e"
sh -c "openssl passwd FpXXrkZ^*fv-tn5PVM$w >> /etc/nginx/htpassw_e"

echo """events {
  worker_connections  1024;
}

http {

  upstream elasticsearch {
    server 127.0.0.1:9201;
  }

  upstream kibana {
    server 127.0.0.1:5601;  
  }

  server {
    listen 9200;

    auth_basic "Protected Elasticsearch";
    auth_basic_user_file /etc/nginx/.htpassw_e;

    location / {
      proxy_pass http://elasticsearch;
      proxy_redirect off;
    }
  }

  server {
    listen 80;
    auth_basic "Protected Kibana";
    auth_basic_user_file /etc/nginx/.htpassw_k;

    location /{
      proxy_pass http://kibana;
      proxy_redirect off;
    }
  }

}

""" > /etc/nginx/nginx.conf