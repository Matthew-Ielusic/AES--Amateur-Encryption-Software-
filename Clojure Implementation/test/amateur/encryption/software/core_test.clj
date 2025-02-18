(ns amateur.encryption.software.core-test
  (:require
    [clojure.test :as t]
    [amateur.encryption.software.core :as sut]))

(t/deftest rotate
  (t/is (= [1 2 3 0] (sut/rotate 1 [0 1 2 3])))
  (t/is (= [2 3 0 1] (sut/rotate 2 [0 1 2 3])))
  (t/is (= [3 0 1 2] (sut/rotate 3 [0 1 2 3])))
  (t/is (= [4 0 1 2 3] (sut/rotate 4 [0 1 2 3 4])))
  (t/is (= [3 0 1 2] (sut/rotate -1 [0 1 2 3]))))
