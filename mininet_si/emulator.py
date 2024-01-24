from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import Topo
import time

sat_num = 2

class Mytopo( Topo ):
    def __init__( self ):
        Topo.__init__(self)

        # Add ground user
        g0 = self.addHost('g0', ip='10.0.1.100/24')

        # Add satellites
        for id in range(1,sat_num+1):
            self.addHost(f'sat{id}', ip=f'10.0.1.{id}/24')

        # Add switches
        switch0 = self.addSwitch('switch0')

        # Create links
        self.addLink(g0, switch0, cls=TCLink)
        for id in range(1,sat_num+1):
            self.addLink(f'sat{id}' , switch0, cls=TCLink)

## type 1: iperf 
# def tcp_data_transfer(src, dst, duration):
    # src.cmd('iperf -s &')
    # time.sleep(2)  # Wait for the server to start

    # print(f"Starting TCP data transfer from {src.name} to {dst.name}")

    # src.cmd(f'iperf -c {dst.IP()} -t {duration}')

## type 2: socket
def tcp_data_transfer(src, dst,duration):
    src.cmd('kill %python')
    dst.cmd('kill %python')

    src.cmd(f'python server.py {src.IP()} &')
    time.sleep(2)  # Wait for the server to start
    print(f"Starting TCP data transfer from {src.name} to {dst.name}")
    dst.cmd(f'python client.py {src.IP()}')

    src.cmd('kill %python')
    dst.cmd('kill %python')

def main():
    
    my_topo = Mytopo()
    net = Mininet(topo=my_topo, link=TCLink)#, controller=None, xterms=False, host=CPULimitedHost, autoPinCpus=True, autoSetMacs=True)

    g0=net.getNodeByName('g0') # same with "g0=net.get('g0')"
    sat1=net.getNodeByName('sat1')
    sat2=net.getNodeByName('sat2')
    
    try:
        # Start the network
        net.start()

        # Initial data transfer
        net.configLinkStatus('switch0', 'sat1', 'up')
        tcp_data_transfer(sat1, g0, 10)

        # Handover (simulate trigger)
        print("Simulating handover...")
        # net.configLinkStatus('switch0', 'sat1', 'down')

        # Pause data transfer during handover
        print("Pausing data transfer during handover...")
        time.sleep(2)  # Simulate handover duration
        
        # Connect to sat2
        net.configLinkStatus('switch0', 'sat2', 'up')
        
        # Resume data transfer
        print("Resuming data transfer after handover...")
        tcp_data_transfer(sat2, g0, 10)
        # net.configLinkStatus('switch0', 'sat2', 'down')

        # Start Mininet CLI
        CLI(net)

    finally:
        net.stop()

if __name__ == '__main__':
    main()
