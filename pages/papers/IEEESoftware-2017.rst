.. title: OTA Updates for Robotic Swarms
.. slug: IEEESoftware/2017/
.. date: 1970-01-01 00:00:00 UTC
.. tags:
.. link: http://www.mistlab.ca/papers/IEEESoftware/2017/
.. description: Secure OTA Updates for Robotic Swarms - IEEE Software (Special Issue Release Engineering 3.0) Supplementary material

.. raw:: html

	<h2>IEEE Software (Special Issue Release Engineering 3.0) Supplementary material</h2>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Real-robot Demonstration</h3>
		</div>
		<div class="panel-body">
			<p>
				<video width="50%" style="float:right;margin-left:50px;min-width:300px;" controls>
					<source src="demonstration.mp4" type="video/mp4">
					Your browser does not support the video tag.
				</video>
				The Video demonstrates a series of field experiments performed with the tool set presented in the paper. During the experiments, the robots were equipped with the ROS implementation of the tool and for the communication an additional package called XbeeMav node was used.
				<br /><br />
				Our ROS implementation is platform-agnostic and was deployed on the <a href="http://wiki.dji.com/en/index.php/Matrice_100" target="_blank">DJI Matrice 100</a>, equipped with a <a href="http://www.nvidia.ca/object/jetson-tk1-embedded-dev-kit.html" target="_blank">NVidia TK1</a> companion computer, <a href="https://3dr.com/solo-drone/" target="_blank">3DR Solo</a> with a <a href="https://www.raspberrypi.org/" target="_blank">Raspberry Pi 3, <a href="https://click.intel.com/intel-aero-ready-to-fly-drone.html" target="_blank">Intel Aero</a> and <a href="https://www.clearpathrobotics.com/husky-unmanned-ground-vehicle-robot/" target="_blank">HUSKY A200</a>. The communication infrastructure between the robots were based on a mesh created by <a href="https://www.digi.com/products/xbee-rf-solutions/sub-1-ghz-modules/xbee-pro-900hp" target="_blank">XBee transceivers</a>.
				<br /><br />
				In the experiments, the robots were commanded to take off and reach a formation using Lennard John’s Potential, a physics based potential function. Despite of certain oscillations, the robots stabilized roughly around their minimum calculated by the potentials.
			</p>
		</div>
	</div>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Update Consensus</h3>
		</div>
		<div class="panel-body">
			<pre style="float:right;width:50%;margin-left:20px;"><code>
	<strong># Create a barrier and set current state as barrier</strong>
	function barrier_set(transf) {
		statef = function() {
			barrier_wait(transf)
		}
		barrier = stigmergy.create(BARRIER_VSTIG) 

	<strong># Add the robot within the barrier</strong>
	function barrier_ready() {
		barrier.put(id, 1)
	}

	<strong># Executes the barrier</strong>
	function barrier_wait(transf) {
		barrier.get(id)
		if(barrier.size() == swarm_size ) {
			<strong># If all robots in barrier
			# proceed to next state</strong>
			statef=transf
		}
	}</code></pre>
			One of the fundamental issues when updating a group of robots during a mission is to reach an agreement on the current version of the code artifact. Indeed, executing multiple version of code artifact could cause undetermined state within the swarm, even more if the code versions alter the way the agents interact with their peers or the environment. A global information agreement mechanism can solve this issue and a convenient approach exists in swarm intelligence, which is inspired from natural environment-mediated communications. Many swarms of insects leave traces in their environment to share information with their neighbors and maintain coordination of the group. This phenomenon is referred to as stigmergy and our implementation is built with the <a href="http://the.swarming.buzz/" target="_blank">Buzz</a> programming primitives of virtual stigmergy. Virtual stigmergy offers a communication-wise method to globally share a (key,value) tuple table among a swarm. 
			<br /><br />
			The agreement over the code version for our solution is achieved with a mechanism based on virtual stigmergy that forces the robots to stay in a specific state until all units agreed to proceed to the state migration. This mechanism is called a barrier, i.e. a protocol for global consensus. A barrier can be implemented in a number of ways, our approach uses virtual stigmergy and swarm construct of Buzz. The swarm construct allows to define groups of robots based on their attributes, track their number and assign them specific actions. 
			<br /><br />
			Our implementation of a barrier is as follow: a virtual stigmergy table is created so that every robot will add an entry to it when they reach the target state. In parallel, a swarm table is created tagging all the robots in the swarm to determine dynamically their number. Once the entries in the virtual stigmergy table equals the number of robots, it is assumed that all the robots reached the target state and are ready for state migration. This code snippet shows such an example of a Buzz script for the barrier.
		</div>
	</div>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Update Security</h3>
		</div>
		<div class="panel-body">
			<table class="table table-sm table-responsive table-striped" style="width:50% !important;float:right;margin-left:20px;">
				<thead class="thead-default">
					<tr>
						<td><strong>Old artifact</strong></td>
						<td><strong>New artifact</strong></td>
						<td><strong>Patch</strong></td>
						<td><strong>Encrypted patch</strong></td>
					</tr>
				</thead>
				<tbody>
					<tr>
						<td>3.3</td>
						<td>4.6</td>
						<td>1.2</td>
						<td>2.5</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>5.6</td>
						<td>2</td>
						<td>4</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>8.5</td>
						<td>4</td>
						<td>8</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>11.5</td>
						<td>6</td>
						<td>12.1</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>14.9</td>
						<td>8</td>
						<td>16.9</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>17</td>
						<td>10</td>
						<td>19.9</td>
					</tr>
					<tr>
						<td>3.3</td>
						<td>30</td>
						<td>20</td>
						<td>37.9</td>
					</tr>
				</tbody>
			</table>

			A major threat that prevails for any updateable system is a device compromise. Moreover, if the device can actuate in the environment (i.e. robots), the damages could be substantial. The threat model within this work considers a man-in-the- middle attack. Every time a new patch is created within the update protocol, the patch is encrypted with a stream cypher called salsa20 and decrypted on reception. 
			<br /><br />
			A stream cypher is used in this solution primarily to increase speed and security but at the cost of larger encrypted stream sizes. One of the drawbacks of stream cypher is to use a unique initialization vector during each encryption. The cypher in this proposed update protocol uses the hash of the previous code versions’ artifact as the initialization vector. This denotes that, the hash of the code artifact from the previous release is required to decrypt the patch from the communication stream. 
			<br /><br />
			In order to hijack the system and inject a malicious patch, a hacker would require the previous releases’ artifact or at least the initial artifact deployed on the robots. This is less likely to happen and hence increases the security of the system.
		</div>
	</div>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Simulations - Static Topology</h2>
		</div>
		<div class="panel-body">
			The communication protocol designed within the simulator corresponds to that of the Xbees. Within the protocol implemented, a series of messages is sent with specific headers to split and merge the data payloads. To request for a list of missing packets the robots use the Acknowledgement messages. The below figures plots the amount of packets exchanged in these two categories.
			<br /><br />
			As explained in our paper, we used three static topologies that simulates and demonstrates the scalability of our approach. The three topologies are: 1. Cluster, 2. Line and 3. Scale free. The rendered view of these topologies from the ARGOS3 Simulator is shown in the first figures and all the other four figures in each class, represent the number of packets exchanged by the robots in four different categories: 1. Acknowledgement messages sent, 2. Acknowledgement messages received, 3. Packets with code sent and 4. packets with code received.

			<hr />

			<h3>Cluster Topology</h3>

			<p>
				<img style="margin:0 auto;display:block" class="img-responsive" src="cluster.png" alt="cluster" />
			</p>

			<table>
				<tr>
					<td>
						<h4>Code packet sent</h4>
						<img src="Code_packet_sent_cluster.png" class="img-responsive" alt="Code packet sent cluster" />
					</td>
					<td>
						<h4>Code packet received</h4>
						<img src="Code_packet_received_cluster.png" class="img-responsive" alt="Code packet received cluster" />
					</td>
				</tr>
				<tr>
					<td>
						<h4>ACK packets sent<h4>
						<img width="100%" src="ACK_packet_sent_cluster.png" class="img-responsive" alt="ACK packet sent cluster" />
					</td>
					<td>
						<h4>ACK packets received<h4>
						<img width="100%" src="ACK_packet_received_cluster.png" class="img-responsive" alt="ACK packet received cluster" />
					</td>
				</tr>
			</table>

			<hr />

			<h3>Line Topology</h3>

			<p>
				<img style="margin:0 auto;display:block" class="img-responsive" src="line.png" alt="line" />
			</p>

			<table>
				<tr>
					<td>
						<h4>Code packet sent</h4>
						<img src="Code_packet_sent_line.png" class="img-responsive" alt="Code packet sent line" />
					</td>
					<td>
						<h4>Code packet received</h4>
						<img src="Code_packet_received_line.png" class="img-responsive" alt="Code packet received line" />
					</td>
				</tr>
				<tr>
					<td>
						<h4>ACK packets sent<h4>
						<img width="100%" src="ACK_packet_sent_line.png" class="img-responsive" alt="ACK packet sent line" />
					</td>
					<td>
						<h4>ACK packets received<h4>
						<img width="100%" src="ACK_packet_received_line.png" class="img-responsive" alt="ACK packet received line" />
					</td>
				</tr>
			</table>

			<hr />

			<h3>Scale-Free Topology</h3>

			<p>
				<img style="margin:0 auto;display:block" src="scalefree.png" class="img-responsive" alt="scalefree" />
			</p>

			<table>
				<tr>
					<td>
						<h4>Code packet sent</h4>
						<img src="Code_packet_sent_scalefree.png" class="img-responsive" alt="Code packet sent scalefree" />
					</td>
					<td>
						<h4>Code packet received</h4>
						<img src="Code_packet_received_scalefree.png" class="img-responsive" alt="Code packet received scalefree" />
					</td>
				</tr>
				<tr>
					<td>
						<h4>ACK packets sent<h4>
						<img width="100%" src="ACK_packet_sent_scalefree.png" class="img-responsive" alt="ACK packet sent scalefree" />
					</td>
					<td>
						<h4>ACK packets received<h4>
						<img width="100%" src="ACK_packet_received_scalefree.png" class="img-responsive" alt="ACK packet received scalefree" />
					</td>
				</tr>
			</table>

		</div>
	</div>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Related Work</h3>
		</div>
		<div class="panel-body">
			The design of a swarm behavior is complex and sometimes results from fortuitous observations of emergent group behaviors. However, swarm is nature's approach to multi-agent systems [1] and thus fascinate numerous robotic research laboratories.
			<br /><br />
			The works of Davis et al. [2] and Chung et al. [3] consist of a ROS-based software controller for a swarm of fixed wing Unmanned Aerial Vehicles' (UAV). The fixed wing UAVs are loaded with a set of behavior binaries before deployment, so the operator selected the adequate binary during flight. The approach was experimented with a swarm of 50 fixed wing UAVs [4]. This system does not allow in-flight installation of new binaries, nor does it integrate a mechanism for global consensus on the current binary.
			<br /><br />
			Hauert et. al. [5] introduced a deployment tool for a flock of fixed-wing UAVs to demonstrate nature-inspired flocking. The deployment platform used IEEE 802.11n protocol for communication but did not provide any mechanism to update the behavior in-flight.
			<br /><br />
			None of the later approaches includes an in-mission update and maintain consistency of the artifacts with a global agreement mechanism. These issues has been broadly addressed in the wireless sensor network (WSN) community. Pilloni et. al. [6] proposed an approach to distribute updates over a WSN with gossip-based routing. Our approach is roughly inspired from this work, but adapted to the actuation and environmental interaction that are specific to robots.
			<br /><br />
			Brown's review [7] details other update solutions for WSNs, from which the most notable approaches are: Trickle, Deluge, MOAP, PDM and Treshnet. These approaches do not take mobility into consideration, since their primary targets are WSNs. In addition, robots need to reach a safe state (e.g. a landed or hovering attitude for a quadcopter) before a controller update can be performed. In our work, we borrow several concepts from these works (e.g. packet management protocols, gossip-based information propagation, and incremental deployment), and apply them to fully-decentralized robotic platforms. 
			<br /><br />
			To the best of our knowledge, none of the existing approaches is fully decentralized, which makes our work a first step in this direction.
			<hr />
			<strong>References:</strong>
			<ol>
				<li>M. Brambilla, E. Ferrante, M. Birattari, and M. Dorigo, “Swarm robotics: A review from the swarm engineering perspective,” Swarm Intelligence, vol. 7, no. 1, pp. 1–41, 2013.</li>
				<li>D. T. Davis, T. H. Chung, M. R. Clement, and M. A. Day, “Consensus- Based Data Sharing for Large-Scale Aerial Swarm Coordination in Lossy Communications Environments,” in IEEE/RSJ International Conference on Intelligent Robots and Systems (IROS), 2016, pp. 3801–3808.</li>
				<li>T. H. Chung, K. D. Jones, M. A. Day, M. Jones, and M. Clement, “50 vs. 50 by 2015: Swarm vs. swarm uav live-fly competition at the naval postgraduate school,” 2013.</li>
				<li>T. H. Chung, M. R. Clement, M. A. Day, K. D. Jones, D. Davis, and M. Jones, “Live-fly, large-scale field experimentation for large numbers of fixed-wing UAVs,” Proceedings - IEEE International Conference on Robotics and Automation, vol. 2016-June, pp. 1255–1262, 2016.</li>
				<li>S. Hauert, S. Leven, M. Varga, F. Ruini, A. Cangelosi, J. C. Zufferey, and D. Floreano, “Reynolds flocking in reality with fixed-wing robots: Commu- nication range vs. maximum turning rate,” IEEE International Conference on Intelligent Robots and Systems, pp. 5015–5020, 2011.</li>
				<li>V. Pilloni, M. Franceschelli, L. Atzori, and A. Giua, “Deployment of Distributed Applications in Wireless Sensor Networks,” IEEE Transactions on Control Systems Technology, vol. 24, no. 5, pp. 1828–1836, 2016. [Online]. Available: <a href="http://www.ncbi.nlm.nih.gov/pubmed/22164024" target="_blank">http://www.ncbi.nlm.nih.gov/pubmed/22164024</a></li>
				<li>S. Brown and C. Sreenan, Software Updating in Wireless Sensor Networks: A Survey and Lacunae, 2013, vol. 2, no. 4. [Online]. Available: <a href="http://www.mdpi.com/2224-2708/2/4/717/" target="_blank">http://www.mdpi.com/2224-2708/2/4/717/</a></li>
			</ol>
		</div>
	</div>


	<div class="panel panel-default">
		<div class="panel-heading">
			<h2 class="panel-title">Relevant Websites and Code Repositories</h3>
		</div>
		<div class="panel-body">
			<ul>
				<li><a href="https://github.com/MISTLab/ROSBuzz" target="_blank">ROS Implemenation of Buzz</a></li>
				<li><a href="https://github.com/MISTLab/XbeeMav" target="_blank">Xbee Node for ROS</li>
				<li><a href="http://the.swarming.buzz/" target="_blank">The Buzz website</a></li>
				<li><a href="https://github.com/MISTLab/Buzz" target="_blank">Buzz run-time and compilation tools</a></li>
				<li><a href="http://www.argos-sim.info/" target="_blank">The ARGoS multi-robot simulator</a></li>
				<li><a href="https://github.com/MISTLab/BuzzKH4" target="_blank">Buzz integration code for Khepera IV</a></li>
				<li><a href="https://github.com/ilpincy/blabbermouth" target="_blank">Blabbermouth: a software hub for inter-robot communication</a></li>
			</ul>
		</div>
	</div>
