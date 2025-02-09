(ns amateur.encryption.software.column-mixer
  "This is a transaltion into clojure of the ColumnMixer.cpp file in the C++ implementation.
   It does some tricky bit manipulation to optimize key steps in the MixColumns operation.")

(def ^:private em 0x1b)
(def ^:private m 0x11b)
(def ^:private m-len 8)

(defn times02
  "Multiplies the input by 0x02, under the field GF(2^8), modulo m(x).
   (That is, XOR-based multiplication.)"
  [byte]
  (let [result (bit-shift-left byte 1)]
    (if (< result 256)
      result
      (bit-xor result m))))

(defn times03
  "Multiplies the input by 0x03, under the field GF(2^8), modulo m(x).
   (That is, XOR-based multiplication.)"
  [byte]
  (let [result (-> byte
                   (bit-shift-left 1)
                   (bit-xor byte))]
    (if (< result 256)
      result
      (bit-xor result m))))