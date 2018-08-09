;; -------------------------------------------------------------------------
;;  File:    moth.lsp
;;  Created: Sun Sep 18 18:09:24 2016
;;  Comment: Library of Mathematical Functions (Pure and Applied).
;; -------------------------------------------------------------------------

(defpackage :moth

  ( :use :common-lisp :slip )

  ( :export 

    :log10
    :one-rad
    :deg->rad
    :even-p
    :fib
    :fact
    :permute
    :choose
    :partition
    :a-divides-b
    :greatest-divisor
    :a-congruent-b-mod-c
    :est-pi-0
    :primep
    :slow-primep
    :sophiep ) )

(in-package moth)

(defconstant one-rad (/ pi 180.0))
(defconstant log10e 2.303)

(defun log10 (n)
  (/ (log n) log10e))

(defun deg->rad (d)
  "Convert radians to degrees."
  (* d one-rad))

(defun even-p(n)
  "Predicate to test if number is even."
  (let ((result nil))
    (setf result (= 0 (mod n 2)))
    result))

(defun fib(n)
  "Compute nth Fibonacci number."
  (if (or (= n 0) (= n 1))
      n
    (+ (fib (- n 1)) (fib (- n 2)))))

(defun fact(n)
  "Compute factorial of n."
  ;(if (= n 1) 1
  ;  (* n (fact (- n 1)))) )
  (if (= n 0) 1
    (reduce #'* 
       (loop for i from 1 to n collect i))))

(defun permute(n k)
  "Compute permution of k items from n items."
  (/ (moth:fact n) (moth:fact (- n k))))

(defun choose(n k)
  "Compute combinations of k items from n items."
  (/ (moth:fact n) 
     (* (moth:fact k) (moth:fact (- n k)))))

(defun partition(n k-list)
  "Compute number of combinations choosing from n items
   and in order choosing k items from k-list"
  (let ((product 1) (x n))
    (loop for k in k-list do
          (format t "~% computing ~a_C_~a" x k)
          (setf product (* product (moth:choose x k)))
          (decf x k))
    product))

; Partition examples:
;
; Twelve different toys are to be distributed among four children,
; giving each child three toys.  How many ways can this be done?
; ans = 369,600

; From a list of 20 problems, a teacher wants to make up three
; homework assignments with six, five, and seven problems. How many
; ways can this be done?
; ans = 2,793,510,720
;

(defun a-divides-b (a b)
  "Test whether a divides b"
  (eq 0 (mod b a)))

(defun greatest-divisor (n)
  "Find greatest divisor of n."
  (let ( (k (1- n)) )
    (loop while (and
                 (not (a-divides-b k n))
                 (>= k 2)) do (decf k)) 
    k))

(defun a-congruent-b-mod-c (a b c)
  "Test whether or not a and b are congurent modulo c.
  This function does a double test, just for educational
  purposes."
  (and (a-divides-b c (- b a))
      (eq (mod a c) (mod b c))))

; Neat estimates for Pi.

(defun est-pi-0 (n) 
  "Estimate pi based on 1/k^2 series."  
  (sqrt (* 6 (float 
      (loop for k from 1 to n 
        sum (/ 1 (expt k 2)))))))

; wrapper around a primality test until we find a good one.

(defun primep(n)
  (slow-primep n))

(defun slow-primep (n)
  "define a brute-force primality test function."
  (if (< n 2)
      nil
    (let ( (results 'nil)
           (divisors (loop for k from 2 to (- n 1) by 1 collect k)) )
      (setf results (mapcar (lambda (x) (a-divides-b x n)) divisors))
      (every #'null results))))

(defun sophiep (n)
  "is n a Sophie Germain Prime?:  2, 3, 5, 11, 23, 29, 41, 53, 83, 89, 113"
  (if (and (moth:primep n) 
           (moth:primep (+ (* 2 n) 1)))
      t))

