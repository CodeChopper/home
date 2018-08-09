;; -------------------------------------------------------------------------
;;  File:    dice.lsp
;;  Created: Sun Sep 18 18:08:36 2016
;;  Comment: Library of Probability and Statistics Functions.
;; -------------------------------------------------------------------------

(defpackage :dice

  ( :use :common-lisp :slip )

  ( :export 
    :binomial-trials
    :poisson
    :entropy-hash
    :p-complement
    :bayes
    :mean-list
    :stddev-list
    :mean-dev-list
    :assign-probs ) )

(in-package dice)

(defun binomial-trials(n k p)
  "Compute probability of k out of n trials succeeding 
   given probability p of success for each trial."
  (* (moth:choose n k) 
     (expt p k) 
     (expt (- 1 p) (- n k))))

(defun poisson(lambda k)
  "Given the average rate (lambda) of a process that varies
  randomly around that rate, compute the Poisson probability
  of k occurrences (instead of lambda occurrences)."
  (/ (* (expt lambda k) (exp (- lambda))) 
     (fact k) ))
     
(defun p-complement (p)
    (- 1.0 p))

(defun mean-list (l)
  "Compute average of list of numbers."
  (if (listp l)
      (float (/ (reduce #'+ l) (length l)))))

(defun stddev-list (l)
  "Compute standard deviation of list of numbers."
  (if (listp l)
      (let* ((n (length l))
             (mean (dice:mean-list l))
             (devs-squared
              (loop for x in l collect (expt (- x mean) 2)))
             (sum-devs-squared (apply #'+ devs-squared)))

        (float (/ sum-devs-squared (- n 1))))))

(defun mean-dev-list (l)
  "Compute mean deviation of list."
  (if (listp l)
      (let* ((mean (dice:mean-list l))
            (mean-devs 
             (loop for x in l collect (abs (- x mean)))))
        (dice:mean-list mean-devs))))

(defun assign-probs (events)
  "Assign random probabilites to a list of events.
   Store probabilities in hash table with event name
   as key."
  (let ((budget 1.0) ; total of probabilities must sum to 1.
        (p 0.0)      ; temp probability for single event.
        (probs (make-hash-table)))

    (loop for e in events do 
          (slip:store-hash probs e 0.0))

    (loop while (> budget 0.0) do
      (setf p (random 0.1))
      (if (> p budget) 
          (setf p budget) )
      (setf choice (slip:random-choice events))    
      (slip:store-hash probs choice 
        (+ (gethash choice probs) p))
      (decf budget p) )
    probs))

(defun entropy-hash (h)
  "Compute the entropy of a hash table. 
   Keys are events/states, values are probabilities.
   (e.g. created by dice:assign-probs)" 
  (let ( (entropy-sum 0.0) 
         (p 0.0) )
    (loop for k being the hash-keys of h do
         (setf p (gethash k h))
         (incf entropy-sum (* p (log p))))
    entropy-sum))





