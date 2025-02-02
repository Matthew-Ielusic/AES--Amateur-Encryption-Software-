(ns amateur.encryption.software.key-schedule-test
  (:require [amateur.encryption.software.key-schedule :as sut]
            [clojure.test :as t]))

(t/deftest rotate
  (t/is (= [1 2 3 0] (sut/rotate [0 1 2 3] 1)))
  (t/is (= [2 3 0 1] (sut/rotate [0 1 2 3] 2)))
  (t/is (= [3 0 1 2] (sut/rotate [0 1 2 3] 3)))
  (t/is (= [4 0 1 2 3] (sut/rotate [0 1 2 3 4] 4))))

(t/deftest word->bytes
  (t/is (= [0x12 0xab 0x48 0x00] (sut/word->bytes 0x12ab4800))))

(t/deftest bytes->word
  (t/is (= 0x0a0b0c0d (sut/bytes->word [0xa 0xb 0xc 0xd]))))

(t/deftest add-Rcon
  (t/is (= [0x46 0xa5 0x15 0xd2] (sut/add-Rcon 36 [0x5d 0xa5 0x15 0xd2]))))

(t/deftest rotate
  (t/is (= [2 3 4 1] (sut/rotate 1 [1 2 3 4]))))


(t/deftest transform-word
  (= 0xd4d1c6f8 (sut/transform-word 0x11f915bc 24)))