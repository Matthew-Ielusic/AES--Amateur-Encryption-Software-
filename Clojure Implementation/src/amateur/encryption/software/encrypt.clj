(ns amateur.encryption.software.encrypt
  (:require
    [amateur.encryption.software.core :as core]
    [amateur.encryption.software.column-mixer :as column-mixer]
    [amateur.encryption.software.key-schedule :as key-schedule]))

(defn shift-rows
  "Takes an array-of-arrays-of-bytes, and executes the ShiftRows operation on it.
   Each nested array represents a row."
  [state]
  (into [] (map-indexed #(core/rotate %1 %2)) state))

(defn mix-column
  "Applies the MixColumns transformation to single column."
  [column]
  (let [mix-fns        [column-mixer/times02 column-mixer/times03 identity identity]
        ; Ensure eager evaluation by using mapv & avoiding `range`:
        value-at-index (fn
                          [idx]
                          (let [rotated (core/rotate-right idx mix-fns)]
                            (apply bit-xor (mapv #((nth rotated %) (nth column %)) [0 1 2 3]))))]
    (mapv value-at-index [0 1 2 3])))

(defn- transpose [state]
  "Takes an array-of-arrays-of-bytes, and transposes the rows and columns."
  (let [make-col-fn (fn [i] (partial mapv #(nth % i)))
        juxt-target (mapv make-col-fn [0 1 2 3])
        transposed  ((apply juxt juxt-target) state)]
    transposed))

(defn mix-columns
  "Takes an array-of-arrays-of-bytes, and executes the MixColumns operation on it.
   Each nested array represents a row."
  [state]
  (->> state
       (transpose)
       (mapv mix-column)
       (transpose)))

