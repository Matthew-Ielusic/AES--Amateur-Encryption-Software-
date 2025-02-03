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
  ; Test case comes from row "i=24" of Appendix A.1
  (t/is (= 0xb9596582 (sut/transform-word 0x11f915bc 24))))

(t/deftest next-word
  ; Test cases come from rows "i=4" and "i=5" of Appendix A.1
  (let [start [0x2b7e1516 0x28aed2a6 0xabf7a588 0x09cf4f3c]
        next  (conj start 0xa0fafe17)]
    (t/is (= 0xa0fafe17 (sut/next-word start 4)))
    (t/is (= 0x88542cb1 (sut/next-word next 5)))))

(t/deftest KeyExpansion
  (t/testing "Simple Cases"
    (let [simple-key (range 16)
          schedule   (sut/KeyExpansion simple-key)]
      (t/is (= 0x00010203 (first schedule)))
      (t/is (= 0x04050607 (second schedule)))
      (t/is (= 0x08090a0b (nth schedule 2)))
      (t/is (= 0x0c0d0e0f (nth schedule 3)))))
  (t/testing "Appendex A.1"
    ; Only test three selected indices, for brevity
    (let [key      [0x2b 0x7e 0x15 0x16 0x28 0xae 0xd2 0xa6 0xab 0xf7 0x15 0x88 0x09 0xcf 0x4f 0x3c]
          _ (tap> key)
          schedule (sut/KeyExpansion key)]
      (t/is (= 0x2b7e1516 (nth schedule 0)))
      (t/is (= 0xdb0bad00 (nth schedule 19)))
      (t/is (= 0xc9ee2589 (nth schedule 41))))))