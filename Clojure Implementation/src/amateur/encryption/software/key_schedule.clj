(ns amateur.encryption.software.key-schedule
  (:require [amateur.encryption.software.core :as core]))

(def Nb 4)  ;; The number of 32-bit words in a "block."  A block is always 4 words.
(def Nk 4)  ;; The number of 32-bit words in the key.  Because I am only implementing 128-bit encryption, Nk = 4.
(def Nr 10) ;; The number of rounds in encryption and decryption.  Is 10 for 128-bit AES.

(defn word->bytes [word]
  "The AES Specification is in terms of 4-byte words, but many operations acton
   single bytes.  Hence functions to go from one to the other.
   My convention is that the leading byte is the most significant."
  [(-> word (bit-and 0xff000000) (bit-shift-right 24))
   (-> word (bit-and 0x00ff0000) (bit-shift-right 16))
   (-> word (bit-and 0x0000ff00) (bit-shift-right 8))
   (-> word (bit-and 0x000000ff))])

(defn bytes->word [bytes]
  "The AES Specification is in terms of 4-byte words, but many operations act on
   single bytes.  Hence functions to go from one to the other.
  My convention is that the leading byte is the most significant."
  (assert (= (count bytes) 4))
  (bit-or (-> bytes (nth 0) (bit-shift-left 24))
          (-> bytes (nth 1) (bit-shift-left 16))
          (-> bytes (nth 2) (bit-shift-left 8))
          (-> bytes (nth 3))))

(defn Rcon-MSB [i]
  "The round 'constant' differs across the key schedule.
   The nth round constant is (2 ** (n - 1)) << 24
   (But remember we are exponentiating using weird XOR-based multiplication!)"
  (cond (< i 0)  (throw (IllegalArgumentException. (str "i must be 0-indexed, was " i)))
        (<= i 8) (bit-shift-left 1 (dec i))
        (= i 9)  0x1b ;; 0x02 ** 8 = 0x80 * 0x02 = 0x1b under AES multiplication
        (= i 10) 0x36
        :else    (throw (IllegalArgumentException. (str "i must be at most 10, was " i)))))

(defn add-Rcon [bytes i]
  "xors the round constant with the input"
  (update bytes 0 #(bit-xor % (Rcon-MSB (/ i Nk)))))

(defn rotate [values n]
  (into (subvec values n) (subvec values 0 n)))

(defn transform-word [word i]
  ;; result = SubWord(RotWord(temp)) xor Rcon[i / Nk]
  (-> word
      word->bytes
      (rotate 1)
      (map core/sbox)
      (add-Rcon i)
      bytes->word))

