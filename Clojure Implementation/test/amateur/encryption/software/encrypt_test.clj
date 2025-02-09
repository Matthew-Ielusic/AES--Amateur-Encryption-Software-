(ns amateur.encryption.software.encrypt-test
  (:require
    [amateur.encryption.software.encrypt :as sut]
    [clojure.test :as t]))

(t/deftest shift-rows
  (let [state [ [0 1 2 3] [4 5 6 7] [8 9 10 11] [12 13 14 15] ]
        expected [ [0 1 2 3] [5 6 7 4] [10 11 8 9] [15 12 13 14] ]]
    (t/is (= expected (sut/shift-rows state)))))