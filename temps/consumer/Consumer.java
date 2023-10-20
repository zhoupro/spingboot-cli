package com.yuaiweiwu.consumer;

import org.apache.kafka.clients.consumer.ConsumerRecord;
import org.springframework.kafka.annotation.KafkaListener;
import org.springframework.stereotype.Component;

@Component
public class Consumer {

    @KafkaListener(topics = "mytopic",groupId = "joke2")
    public void listen(ConsumerRecord<?, ?> cr) throws Exception {
        Object value = cr.value();
        Object key = cr.key();
        System.out.println(key);
        System.out.println(value);
    }
}
