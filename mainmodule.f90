module variables_module

implicit none

integer, parameter :: num_vars = 5

integer :: amount
real :: pi
complex :: frequency
character(len=1) :: initial
logical :: isOkay

contains

subroutine initialize_variables()

  amount = 10
  pi = 3.1415927
  frequency = (1.0, -0.5)
  initial = 'A'
  isOkay = .false.

end subroutine initialize_variables

subroutine print_variables()

  integer :: i

  do i = 1, 5
    select case(i)
      case(1)
        print *, 'amount = ', amount
      case(2)
        print *, 'pi = ', pi
      case(3)
        print *, 'frequency = ', frequency
      case(4)
        print *, 'initial = ', initial
      case(5)
        print *, 'isOkay = ', isOkay
    end select
  end do

end subroutine print_variables

end module variables_module

program main

use variables_module

call initialize_variables()
call print_variables()

end program main
