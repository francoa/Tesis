simuStack
=========

Stack of lammps simulatins to run, which can be updated dynamically.

Notes
===============

 - The command list is cleaned upon reset of the stack. DON'T erease lines of this file, just add them in the end.
 - You can see what's going on in the file _logSimuStack_
 - The command list is automatically updated with the most recent restart file 
 - The restart input file is updated with the pending operations

Compiling
==========

~$ make

Running
=========

~$ ./simuStack &

Adding commands
===============

Edit the file _simuList_ and add lines with this pattern:

          #cd path/to/simulation/directory
          mpirun -n 8 lmp_openmpi < yourInputFile.in > yourOutputFile.out
                    
Recommended: create a temporary file with the command and then
          
          cat cmdTempFile >> path/to/simuList
          
The list after reset
====================

If your simulation was stopped at step=140000, the restart file was 
written at step=130000 and your current fix started in step=120000 and
had to do 50000 steps, the new list would be:

		#cd path/to/simulation/directory
		mpirun -n 8 lmp_openmpi < yourInputFile.restart.130000.in > yourOutputFile.restart.130000.out
		
and the new input file will set the run of the pending fix to 40000, and add
all the rest of the fixes.

Input conventions
=================

		#THERMO_INFO
		thermo 
		thermo
		thermo
		#END_THERMO_INFO
		
		#OP
		fix F1 etc
		dump ID etc
		restart	10000 etc
		[...]
		
		#OP
		fix F2 etc
		[...]
          
If two different code blocks (run command) use the same fix, let the stack
know this by adding an empty comment line where a fix should be placed. This allows
the proper computation of run command's steps left.

		#OP
		#

When a stopped simulation is found, this program searches for a file called
_input.restart.in_ that is a template with the common information for all
simulation fixes. Then it adds to this template the pending operations and
stores the new file in input.restart.STEP.in WITHOUT modifying the template.
It is necessary to leave a template file for this program to work.
