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

(defn Rcon-MSB
  "The round 'constant' differs across the key schedule.
   The nth rcon is (2 ** (n - 1)) << 24
   (But remember we are exponentiating using weird XOR-based multiplication!)"
  [i]
  (let [index (int (/ i Nk))]
    (cond (< index 0) (throw (IllegalArgumentException. (str "i must be 0-indexed, was " i)))
          (<= index 8) (bit-shift-left 1 (dec index))
          (= index 9) 0x1b                                       ;; 0x02 ** 8 = 0x80 * 0x02 = 0x1b under AES multiplication
          (= index 10) 0x36
          :else (throw (IllegalArgumentException. (str "i must be at most 40, was " i))))))

(defn add-Rcon
  "xors the round constant with the input"
  [i bytes]
  (update bytes 0 #(bit-xor % (Rcon-MSB i))))

(defn rotate [n values]
  (into (subvec values n) (subvec values 0 n)))

(defn transform-word
  "Takes a 32-bit word and the round number i, and applies the transformation
   `result = SubWord(RotWord(temp)) xor Rcon[i / Nk]`"
  [word i]
  {:pre [(int? word) (<= 4 i 43)]}
  (->> word
      word->bytes
      (rotate 1)
      (mapv core/sbox)
      (add-Rcon i)
      bytes->word))

