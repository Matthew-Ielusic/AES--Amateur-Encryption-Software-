(ns amateur.encryption.software.encrypt
  (:require
    [amateur.encryption.software.core :as core]
    [amateur.encryption.software.key-schedule :as key-schedule]))

(defn shift-rows
  "Takes an array-of-arrays-of-bytes, and executes the ShiftRows operation on it.
   Each nested array represents a row."
  [state]
  (into [] (map-indexed #(core/rotate %1 %2)) state))


