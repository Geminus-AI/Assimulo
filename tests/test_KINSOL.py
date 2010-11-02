import nose
import numpy as N
from assimulo.problem_algebraic import *
from assimulo.kinsol import *


class Test_KINSOL:
    
    def setUp(self):
        
        """
        sets up the test case
        """
        
        
        
        class Prob1(ProblemAlgebraic):
            f = lambda self, x:N.array([x[0]-1.0, x[1]-2.0,x[2]-3.0])
            _x0 = [0.0,0.0,0.0]
            
            def set_x0(self,x0):
                self._x0 = x0
                
            def get_x0(self):
                return self._x0
        self.p1 = Prob1()
        self.solve_p1 = KINSOL(self.p1)
        
        class Prob_no_f(ProblemAlgebraic):
            _x0 = [0.0,0.0,0.0]
            
            def set_x0(self,_x0):
                self._x0 = x0
                
            def get_x0(self):
                return self._x0
            
        self.no_f = Prob_no_f()
        #self.solve_no_f = KINSOL(self.no_f)
        
        class Prob_no_x0(ProblemAlgebraic):
            f = lambda self, x:N.array([x[0]-1.0, x[1]-2.0,x[2]-3.0])
            
            def set_x0(self,x0):
                self._x0 =x0
                
            def get_x0(self):
                return self._x0
            
        self.no_x0 = Prob_no_f()
        #self.solve_no_x0 = KINSOL(self.no_x0)
        
        class Prob_no_getx0(ProblemAlgebraic):
            f = lambda self, x:N.array([x[0]-1.0, x[1]-2.0,x[2]-3.0])
            _x0 = [0.0,0.0,0.0]
            
            def set_x0(self,x0):
                self._x0 = x0
                
        self.no_getx0 = Prob_no_getx0()
        #self.solve_no_getx0 = KINSOL(self.no_getx0)
        
        class Prob_Jac(ProblemAlgebraic):
            f = lambda self, x:N.array([x[0]-1.0, x[1]-2.0,x[2]-3.0])
            _x0 = [0.0,0.0,0.0]
            jac_called = False
            
            def jac(self,x):
                self.jac_called = True
                print "Jacobian called"
                return N.zeros(3)
            
            def set_x0(self,x0):
                self._x0 = x0
                
            def get_x0(self):
                return self._x0
            
        self.pb_jac = Prob_Jac()
        self.solve_pb_jac = KINSOL(self.pb_jac)
        
        class Prob_Const(ProblemAlgebraic):
            f = lambda self, x:N.array([-(x[0]-1.0)**2 +4, x[1]-2.0,x[2]-3.0])
            _x0 = [0.0,1.0,1.0]
            _const = None
            
            def set_x0(self,x0):
                self._x0 = x0
                
            def get_x0(self):
                return self._x0
            
            def set_constraints(self,const):
                self._const = const
                
            def get_constraints(self):
                return self._const
                
        self.pb_const = Prob_Const()
        self.solve_pb_const = KINSOL(self.pb_const)
        
          
    def test_solve(self):
        """
        Test if solve works in kinsol.py
        """
        
        # tests for problems without all member attributes/methods
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.no_f)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.no_x0)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.no_getx0)
        
        # test solver for simple problem
        res = self.solve_p1.solve()
        nose.tools.assert_almost_equal(res[0],1.0,5)
        nose.tools.assert_almost_equal(res[1],2.0,5)
        nose.tools.assert_almost_equal(res[2],3.0,5)
        
        self.p1.set_x0('a string')
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.p1)
        
        self.p1.set_x0(5)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.p1)
        
        self.p1.set_x0(0.6)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL, self.p1)
        
    def test_jac_usage(self):
        """
        Tests if user-supplied jacobians are implemented correctly in kinsol.py
        """
        # test is supplied jacobian is called
        try:
            self.solve_pb_jac.set_jac_usage(True)
            self.solve_pb_jac.solve()
        except :
            pass
        
        nose.tools.assert_true(self.pb_jac.jac_called,'Jacobian not used although use_jac = true')
        
        self.pb_jac.jac_called = False
        try:
            self.solve_pb_jac.set_jac_usage(False)
            self.solve_pb_jac.solve()
        except :
            pass
        
        nose.tools.assert_false(self.pb_jac.jac_called,'Jacobian used although use_jac = false')
        
    def test_constraints_usage(self):
        """
        Tests if constraints are implemented correctly in kinsol.py
        """
        res =self.solve_pb_const.solve()
        nose.tools.assert_almost_equal(res[0],-1.0,5)
        nose.tools.assert_almost_equal(res[1],2.0,5)
        nose.tools.assert_almost_equal(res[2],3.0,5)
        
        self.pb_const.set_constraints(5)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints('a')
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints(True)
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints([1.,1.,1.])
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints(N.ones(2))
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints(N.ones(3,dtype = int))
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints(-N.ones(3,dtype = float))
        nose.tools.assert_raises(KINSOL_Exception,KINSOL,self.pb_const)
        
        self.pb_const.set_constraints(N.ones(3))
        print "const: ",self.pb_const._const
        self.pb_const.set_x0(N.array([1.5,1.0,1.0]))
        self.solve_pb_const = KINSOL(self.pb_const)
        
        res2 = self.solve_pb_const.solve()
        nose.tools.assert_almost_equal(res2[0],3.0,5)
        nose.tools.assert_almost_equal(res2[1],2.0,5)
        nose.tools.assert_almost_equal(res2[2],3.0,5)
        
    def test_printlevel_usage(self):
        """
        test if the setting of printout level works
        """
        # test default value
        nose.tools.assert_equal(self.solve_p1.print_level,0)
        
        # Test for faulty input
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,1.0)
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,True)
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,'a')
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,4)
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,-1)
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,N.ones(3))
        nose.tools.assert_raises(KINSOL_Exception,self.solve_p1.set_print_level,N.ones(3,dtype = int))
        
        # Test if set correctly
        self.solve_p1.set_print_level(1)
        nose.tools.assert_equal(self.solve_p1.print_level,1)
        
        self.solve_p1.set_print_level(2)
        nose.tools.assert_equal(self.solve_p1.print_level,2)
        
        self.solve_p1.set_print_level(3)
        nose.tools.assert_equal(self.solve_p1.print_level,3)
        
        self.solve_p1.set_print_level(0)
        nose.tools.assert_equal(self.solve_p1.print_level,0)

        
        
        