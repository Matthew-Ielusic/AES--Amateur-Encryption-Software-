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

(defn times09
  "Multiplies the input by 0x09, under the field GF(2^8), modulo m(x).
   (That is, XOR-based multiplication.)"
  [byte]
  ; Imperative for loop:
  ;     for (int shift = 3; result >= 256; --shift) {
  ;        //if (result > (m << shift))
  ;        if (result & (1 << (shift + mLen)))
  ;            result ^= m << shift;
  ;    }
  ; Clojure translation of the above:
  (loop [result (-> byte (bit-shift-left 3) (bit-xor byte))
         shift 3]
    (prn "result:")
    (prn result)
    (prn "shift:")
    (prn shift)
    (let [result' (if (not=
                        0
                        (bit-and
                          result
                          (bit-shift-left
                            1
                            (+ shift m-len))))
                    (bit-xor result (bit-shift-left m shift))
                    result)]
      (if (>= result' 256)
        (recur
          result'
          (dec shift))
        (mod result' 256))))
  ; Clojure was *not* built to do bit manipulations in a for loop
  ; TODO: Find a new formula for this, that is implemented without a horrible awful no-good imperative for loop
  )
