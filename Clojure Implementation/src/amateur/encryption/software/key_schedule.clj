(ns amateur.encryption.software.key-schedule
  (:require [amateur.encryption.software.core :as core]))

(def Nb 4)  ;; The number of 32-bit words in a "block."  A block is always 4 words.
(def Nk 4)  ;; The number of 32-bit words in the key.  Because I am only implementing 128-bit encryption, Nk = 4.
(def Nr 10) ;; The number of rounds in encryption and decryption.  Is 10 for 128-bit AES.

(defn word->bytes [word]
  "The AES Specification is in terms of 4-byte words, but many operations act on
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

(defn transform-word
  "Takes a 32-bit word and the round number i, and applies the transformation
   `result = SubWord(RotWord(temp)) xor Rcon[i / Nk]`"
  [word i]
  {:pre [(int? word) (<= 4 i 43)]}
  (->> word
      word->bytes
      (core/rotate 1)
      (mapv core/sbox)
      (add-Rcon i)
      bytes->word))

(defn next-word
  "Take a partial key schedule, and the current index of iteration, and returns what the next word in the key schedule will be."
  [key-schedule i]
  (let [temp       (last key-schedule) ; "temp" being the variable name in the specification pseudocode
        temp'      (if (= 0 (mod i Nk))
                     (transform-word temp i)
                     temp)
        xor-target (nth key-schedule (- i Nk))]
    (bit-xor xor-target temp')))

(defn KeyExpansion
  "Takes a sequence of sixteen bytes, representing the 128-bit key, and returns a vector of forty-four 32-bit words.
   The capitalization follows the capitalization used in the specification document."
  [key]
  {:pre [(sequential? key) (= 16 (count key))]}
  (let [initial (mapv bytes->word (partition 4 key))]
    (reduce #(conj %1 (next-word %1 %2)) initial (range 4 44))))

(defn add-round-key [state key-schedule round-num]
  "Takes the state, as an array-of-array-of-bytes, the expanded key, and the current round number, and returns the result of adding the round key to the state."
  (let [xform (comp (drop (* round-num 4))                  ; Start at, in the words of the specification, round * Nb
                    (take 4)                                ; Take 4 words from the key schedule
                    (map word->bytes))
        bytes (into [] xform key-schedule)]
    ; So we have two vectors-of-vectors-of-bytes... state & "bytes"
    ; We just want to XOR them together.
    (tap> "bytes:")
    (tap> bytes)
    (mapv
      (partial mapv bit-xor)
      state
      bytes)))