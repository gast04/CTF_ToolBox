; tries to implement faculty into z3

; ****************************************************
; simple way did not work, obviously there
; is no faculty operator, tried: (x-1)!*x;
; (faculty for negative numbers is not defined)
(declare-const x Int)
(assert (>= x 0))
(assert (= (! x) 24))
(check-sat)
(get-model)

; ****************************************************
; implement the faculty function
(declare-fun f (Int) Int)
(declare-const x Int)
(assert (= (f 0) 1))
(assert (= (f 1) 1))
(assert (>= x 2) )
(assert (= (f x) (* x (f (- x 1))  )))
(check-sat)
(get-model)
; resume: did not work because x is a constant and not
; all natural numbers...


; ****************************************************
; found in the docs that z3 will not do inductive proofs
; but this is exactly what we would need...
; forall x in Nat : f(x) == x*f(x-1)

; this is an inductive example which will not work
; (inductive proofs are future work)
(set-option :timeout 2000)
(declare-datatypes () ((Nat zero (succ (pred Nat)))))
(declare-fun p (Nat) Bool)
(assert (p zero))
(assert (forall ((x Nat)) (implies (p (pred x)) (p x))))
(assert (not (forall ((x Nat)) (p x))))
(check-sat)
(get-info :all-statistics)
