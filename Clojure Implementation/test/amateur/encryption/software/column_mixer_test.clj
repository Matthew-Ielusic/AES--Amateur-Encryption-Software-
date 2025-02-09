(ns amateur.encryption.software.column-mixer-test
  (:require
    [amateur.encryption.software.column-mixer :as sut]
    [clojure.test :as t]))

(t/deftest times02
  (t/is (= 16 (sut/times02 8)))
  (t/is (= 0x39 (sut/times02 0x91)))
        ; 0x91 -> x^7 + x^4 + 1
        ; 0x91 * 0x02 -> (x^8 + x^5 + x) mod m(x)
        ; m(x) = x^8 + x^4 + x^3 + x + 1
        ; 0x91 * 0x02 -> x^5 + x^4 + x^3 + 1 -> 0x39
        )

(t/deftest times03
  (t/is (= 24 (sut/times03 8)))
  (t/is (= 20 (sut/times03 12)))
  (t/is (= 0xb0 (sut/times03 0x99)))
        ; 0x99 -> x^7 + x^4 + x*3 + 1
        ; 0x99 * 0x03 -> [(x^8 + x^5 + x^4 + x) + (x^7 + x^4 + x^3 + 1)] mod m(x)
        ; 0x99 * 0x03 -> x^8 + x^7 + x^5 + x^3 + x + 1 mod m(x)
        ; m(x) = x^8 + x^4 + x^3 + x + 1
        ; 0x99 * 0x03 -> x^7 + x^5 + x^4 -> 0xb0
        )

(t/deftest times09
  ; Expected values come from this Galois calculator: http://www.ee.unb.ca/cgi-bin/tervo/calc2.pl
  (t/is (= 9 (sut/times09 0x01)))
  (t/is (= 0x5a (sut/times09 0xa)))
  (t/is (= 0x1c (sut/times09 0xf5))))