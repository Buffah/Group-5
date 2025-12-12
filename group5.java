
import java.util.*; 
import java.time.Instant; 
 

// Packet class 

class Packet { 
    private int pktId; 
    private String src; 
    private String dst; 
    private int sizeBytes; 
    private long timestamp; 
 
    public Packet(int pktId, String src, String dst, int sizeBytes) { 
        this.pktId = pktId; 
        this.src = src; 
        this.dst = dst; 
        this.sizeBytes = sizeBytes; 
        this.timestamp = Instant.now().toEpochMilli(); 
    } 
 
    public double sizeMB() { 
        return (double) sizeBytes / (1024 * 1024); 
    } 
 
    public int getPktId() { 
        return pktId; 
    } 
} 
 
// Abstract base class: NetworkNode 

abstract class NetworkNode { 
    protected String nodeId; 
    protected List<Packet> queue = new ArrayList<>(); 
 
    public NetworkNode(String nodeId) { 
        this.nodeId = nodeId; 
    } 
 
    public void receivePacket(Packet pkt) { 
        queue.add(pkt); 
    } 
 
    public int queueLength() { 
        return queue.size(); 
    } 
 
    public abstract Packet forwardPacket(NetworkNode dstNode); 
} 
 

// RouterNode subclass 

class RouterNode extends NetworkNode { 
    protected Map<String, String> routingTable = new HashMap<>(); 
 
    public RouterNode(String nodeId) { 
        super(nodeId); 
    } 
 
    @Override 
    public Packet forwardPacket(NetworkNode dstNode) { 
        // Simple FIFO forwarding 
        if (!queue.isEmpty()) { 
            Packet pkt = queue.remove(0); 
            dstNode.receivePacket(pkt); 
            return pkt; 
        } 
        return null; 
    } 
 
    public void updateRoutingTable(String dst, String nextHop) { 
        routingTable.put(dst, nextHop); 
    } 
} 
 

// CoreRouter subclass 

class CoreRouter extends RouterNode { 
 
    public CoreRouter(String nodeId) { 
        super(nodeId); 
    } 
 
    public void optimizeRouting() { 
        System.out.println("[CoreRouter " + nodeId + "] Optimizing routing table..."); 
        // Placeholder for real algorithm 
    } 
 
    @Override 
    public Packet forwardPacket(NetworkNode dstNode) { 
        Packet pkt = super.forwardPacket(dstNode); 
        if (pkt != null) { 
            System.out.println("[CoreRouter " + nodeId + "] Forwarded packet " 
                    + pkt.getPktId() + " with optimized path"); 
        } 
        return pkt; 
    } 
} 
 

// EdgeRouter subclass 

class EdgeRouter extends RouterNode { 
 
    public EdgeRouter(String nodeId) { 
        super(nodeId); 
    } 
 
    @Override 
    public Packet forwardPacket(NetworkNode dstNode) { 
        if (!queue.isEmpty()) { 
            Packet pkt = queue.remove(0); 
 
            // Drop if larger than 2MB 
            if (pkt.sizeMB() > 2) { 
                System.out.println("[EdgeRouter " + nodeId + 
                        "] Dropped packet " + pkt.getPktId() + " due to size limit"); 
                return null; 
            } 
 
            dstNode.receivePacket(pkt); 
            System.out.println("[EdgeRouter " + nodeId + "] Forwarded packet " 
                    + pkt.getPktId() + " with QoS rules"); 
            return pkt; 
        } 
        return null; 
    } 
} 
 

// Example Simulation (main) 

public class TelecomSimulation { 
    public static void main(String[] args) { 
 
        // Create nodes 
        CoreRouter core = new CoreRouter("Core1"); 
        EdgeRouter edge = new EdgeRouter("Edge1"); 
        RouterNode hostDst = new RouterNode("H2"); 
 
        // Create packets 
        Packet pkt1 = new Packet(401, "H1", "H2", 1_000_000); 
        Packet pkt2 = new Packet(402, "H1", "H2", 3_000_000); 
 
        // Queue packets in edge router 
        edge.receivePacket(pkt1); 
        edge.receivePacket(pkt2); 
 
        // Forward: edge -> core -> host 
        edge.forwardPacket(core);   
        edge.forwardPacket(core); 
 
        core.forwardPacket(hostDst); 
        core.forwardPacket(hostDst); 
 
        // Inspect queue lengths 
System.out.println("Host/Destination queue length: " + 
hostDst.queueLength()); 
} 
}
