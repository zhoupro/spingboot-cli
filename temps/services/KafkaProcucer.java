package {{packageName}}.services;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.kafka.core.KafkaTemplate;
import org.springframework.stereotype.Service;


@Service
public class KafkaProcucer {
    @Autowired
    private  KafkaTemplate<String,String > temp;

    public  void Send(String msg) {
        temp.send("mytopic", "mytest", msg);
    }
}
