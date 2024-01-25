from mininet.net import Mininet
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.topo import Topo
import time
from threading import Thread, Event

sat_num = 2
handover_interval = 5

triggered = Event()

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

def run_tcp_server(server):
    server.cmd(f'python server.py {server.IP()} &')
    time.sleep(2)

def stop_tcp_server(server):
    server.cmd('kill %python')

def start_tcp_trasfer(server, client):
    print(f"Starting TCP data transfer from {client.name} to {server.name}")
    triggered.clear()
    while True:
        if not triggered.is_set():
           dst.cmd(f'python client.py {server.IP()}')

def freeze_tcp_transfer(process):
    triggered.set()

def handover(net, egress_sat, ingress_sat):
    stop_tcp_server(egress_sat)
    net.configLinkStatus('switch0', egress_sat, 'down')
    net.configLinkStatus('switch0', ingress_sat, 'up')
    run_tcp_server(ingress_sat)

def initialize_link(net):
    # activate sat1
    net.configLinkStatus('switch0', 'sat1', 'up')
    # deactivate others
    for id in range(1,sat_num+1):
        net.configLinkStatus('switch0' , f'sat{id}', 'down')


def main():
    
    my_topo = Mytopo()
    net = Mininet(topo=my_topo, link=TCLink)#, controller=None, xterms=False, host=CPULimitedHost, autoPinCpus=True, autoSetMacs=True)

    g0=net.getNodeByName('g0') # same with "g0=net.get('g0')"
    sat1=net.getNodeByName('sat1')
    sat2=net.getNodeByName('sat2')
    
    initialize_link(net)
    try:
        # Start the network
        net.start()

        # Run tcp server
        ingress_sat = sat1
        run_tcp_server(ingress_sat)

        # data transfer # multiprocessing
        t=Thread(target=start_tcp_tranfer,args=(ingress_sat, g0))
        t.start()

        print("Simulating handover...")
        while True:
            # Pause data transfer during handover
            print("Pausing data transfer during handover...")
            freeze_tcp_transfer(g0)
            t.join()

            # Handover (simulate trigger)
            egress_sat = sat2
            handover(net, egress_sat, ingress_sat)

            # Resume data transfer
            print("Resuming data transfer after handover...")
            t=Thread(target=start_tcp_tranfer,args=(ingress_sat, g0))
            t.start()

            time.sleep(handover_interval)
            
        # Start Mininet CLI
        CLI(net)

    finally:
        net.stop()

if __name__ == '__main__':
    main()
