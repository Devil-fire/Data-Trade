pragma solidity ^0.4.24;

contract Controller {

    address[] private projects;
    address public cloud;
    uint256 private amount;

    constructor() public
    {
        amount = 0;
        cloud = msg.sender;
    }

    event newscheme(address);

    function createProject(uint256 bpk0,uint256 bpk1,
    uint256 tw0, uint256 tw1, uint256 tw2, uint256 tw3) public returns(address)
    {
        address newProject = new scheme(bpk0, bpk1, tw0, tw1, tw2, tw3, cloud, msg.sender);
        projects.push(newProject);
        amount += 1;
        emit newscheme(newProject);
        return newProject;
    }

    function getProjects() public view returns(address[])
    {
        return projects;
    }

    function getAmount() public view returns(uint256)
    {
        return amount;
    }

}


contract scheme{

    enum State {
        init, twsent, rksent, hssent, tksent, ciphersent, paid, closed
    }


    uint256[2] public buyerpk;
    address private buyer;
    uint256[2] public sellerpk;
    address private seller;
    address private cloud;
    uint256[4] public TW;
    uint256[2] public RK;
    uint256 public HASHOFC3;
    uint256[4] public TK;
    uint256 public PRICE;
    uint256 private WEITOETH  = 1000000000000000000;
    uint256 private FORSELLER = 900000000000000000;
    uint256 private FORCLOUD  = 100000000000000000;
    State private state;
    uint256[2] public C1;
    uint256[4] public C2;
    uint256[12] public C3;
    uint256[12] public C4;

    modifier inState(State _state){
        require(state == _state, "invalid state.");
        _;
    }
    modifier selleronly(){
        require(msg.sender == seller, "seller only");
        _;
    }
    modifier buyeronly(){
        require(msg.sender == buyer, "buyer only");
        _;
    }
    modifier cloudonly(){
        require(msg.sender == cloud, "cloud only");
        _;
    }
    modifier enoughmoney(){
        require(msg.value == mul(PRICE, WEITOETH), "not enough money");
        _;
    }
    function mul(uint256 a, uint256 b) internal pure returns(uint256){
        if (a == 0){
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }

    constructor(uint256 bpk0,uint256 bpk1,
    uint256 tw0, uint256 tw1, uint256 tw2, uint256 tw3, address CLD, address BUY)
    public
    {
        state = State.twsent;
        cloud = CLD;
        buyer = BUY;
        buyerpk[0] = bpk0;
        buyerpk[1] = bpk1;
        TW[0] = tw0;
        TW[1] = tw1;
        TW[2] = tw2;
        TW[3] = tw3;
    }

    function PermitSearch(uint256 spk0, uint256 spk1,
    uint256 rk0, uint256 rk1)
    public
    inState(State.twsent)
    {
        state = State.rksent;
        seller = msg.sender;
        sellerpk[0] = spk0;
        sellerpk[1] = spk1;
        RK[0] = rk0;
        RK[1] = rk1;
    }

    function SearchDone(uint256 c3, uint256 price)
    public
    cloudonly
    inState(State.rksent)
    {
        state = State.hssent;
        HASHOFC3 = c3;
        PRICE = price;
    }

    function pay()
    public
    payable
    buyeronly
    enoughmoney
    inState(State.hssent)
    {
        state = State.paid;
    }

    function PermitReEnc(uint256 tk0, uint256 tk1, uint256 tk2, uint256 tk3)
    public
    selleronly
    inState(State.paid)
    {
        state = State.tksent;
        TK[0] = tk0;
        TK[1] = tk1;
        TK[2] = tk2;
        TK[3] = tk3;
    }

    function Confirm()
    public
    inState(State.tksent)
    buyeronly
    {
        state = State.closed;
        seller.transfer(mul(PRICE, FORSELLER));
        cloud.transfer(mul(PRICE, FORCLOUD));
    }


    function Test(uint256 c10, uint256 c11,
	  uint256 tk0, uint256 tk1, uint256 tk2, uint256 tk3,
	  uint256 rk0, uint256 rk1,
	  uint256 c20, uint256 c21, uint256 c22, uint256 c23)
	private
	view
	returns (bool)
	{
	    G1Point[] memory p1 = new G1Point[](2);
	    G2Point[] memory p2 = new G2Point[](2);

        p1[0].X=c10;
        p1[0].Y=c11;

        p2[0].X[1]=tk0;
        p2[0].X[0]=tk1;
        p2[0].Y[1]=tk2;
        p2[0].Y[0]=tk3;

        p1[1].X=rk0;
        p1[1].Y=rk1;

        p2[1].X[1]=c20;
        p2[1].X[0]=c21;
        p2[1].Y[1]=c22;
        p2[1].Y[0]=c23;

	    bool b = pairingProd2(p1[0], p2[0], g1neg(p1[1]), p2[1]);

	    return b;
	}

	function Sendc1(uint256 c10, uint256 c11)
	public
	inState(State.tksent)
	cloudonly
	{
	    C1[0] = c10;
        C1[1] = c11;
	}

	function Sendc2(uint256 c20, uint256 c21, uint256 c22, uint256 c23)
	public
	inState(State.tksent)
	cloudonly
	{
	    C2[0] = c20;
        C2[1] = c21;
        C2[2] = c22;
        C2[3] = c23;
	}

	function Sendc3(uint256 c30, uint256 c31, uint256 c32, uint256 c33,
    uint256 c34, uint256 c35, uint256 c36, uint256 c37,
    uint256 c38, uint256 c39, uint256 c310, uint256 c311)
	public
	inState(State.tksent)
	cloudonly
	{
	    C3[0] = c30;
        C3[1] = c31;
        C3[2] = c32;
        C3[3] = c33;
        C3[4] = c34;
        C3[5] = c35;
        C3[6] = c36;
        C3[7] = c37;
        C3[8] = c38;
        C3[9] = c39;
        C3[10] = c310;
        C3[11] = c311;
	}

	function Sendc4(uint256 c40, uint256 c41, uint256 c42, uint256 c43,
    uint256 c44, uint256 c45, uint256 c46, uint256 c47,
    uint256 c48, uint256 c49, uint256 c410, uint256 c411)
	public
	inState(State.tksent)
	cloudonly
	{
	    C4[0] = c40;
        C4[1] = c41;
        C4[2] = c42;
        C4[3] = c43;
        C4[4] = c44;
        C4[5] = c45;
        C4[6] = c46;
        C4[7] = c47;
        C4[8] = c48;
        C4[9] = c49;
        C4[10] = c410;
        C4[11] = c411;
	}

    function GetMoney()
    public
    cloudonly
    inState(State.tksent)
    {
        if(compare1() && compare2())
        {
            seller.transfer(mul(PRICE, FORSELLER));
            cloud.transfer(mul(PRICE, FORCLOUD));
        }
        state = State.closed;
    }

    function GetState()
    public
    view
    returns(State)
    {
        return (state);
    }

    function GetPubkey()
    public
    view
    returns(uint256[2])
    {
        return (buyerpk);
    }

    function GetTrapdoor()
    public
    view
    returns(uint256[4])
    {
        return (TW);
    }

    function GetReKey()
    public
    cloudonly
    view
    returns(uint256[2])
    {
        return (RK);
    }

    function GetToken()
    public
    cloudonly
    view
    returns(uint256[4])
    {
        return (TK);
    }

    function compare1() private view returns (bool)
    {
        bool b = Test(C1[0], C1[1], TK[0], TK[1], TK[2], TK[3],
                      RK[0], RK[1], C2[0], C2[1], C2[2], C2[3]);
        return b;
    }

    function compare2() private view returns (bool)
    {
        uint256 c4 = 0;
        for(uint i = 0; i < 12; i++){
            c4 += C4[i];
        }
        bytes32 b1 = keccak256(uint2str(c4));
        bytes32 b2 = bytes32(HASHOFC3);
        if(b1 == b2)
        {
            return true;
        }
        else
        {
            return false;
        }
    }

    function uint2str(uint i) pure private returns (string c) {
        if (i == 0) return "0";
        uint j = i;
        uint length;
        while (j != 0){
            length++;
            j /= 10;
        }
        bytes memory bstr = new bytes(length);
        uint k = length - 1;
        while (i != 0){
            bstr[k--] = byte(48 + i % 10);
            i /= 10;
        }
        c = string(bstr);
    }

	struct G1Point {
		uint X;
		uint Y;
	}

	struct G2Point {
		uint[2] X;
		uint[2] Y;
	}

	function g1neg(G1Point p) pure internal returns (G1Point) {
		uint q = 21888242871839275222246405745257275088696311157297823662689037894645226208583;
		if (p.X == 0 && p.Y == 0)
			return G1Point(0, 0);
		return G1Point(p.X, q - (p.Y % q));
	}

	function pairing(G1Point[] p1, G2Point[] p2) constant internal returns (bool) {
		require(p1.length == p2.length);
		uint elements = p1.length;
		uint inputSize = elements * 6;
		uint[] memory input = new uint[](inputSize);
		for (uint i = 0; i < elements; i++)
		{
			input[i * 6 + 0] = p1[i].X;
			input[i * 6 + 1] = p1[i].Y;
			input[i * 6 + 2] = p2[i].X[0];
			input[i * 6 + 3] = p2[i].X[1];
			input[i * 6 + 4] = p2[i].Y[0];
			input[i * 6 + 5] = p2[i].Y[1];
		}
		uint[1] memory out;
		bool success;
		assembly {
			success := staticcall(sub(gas, 2000), 8, add(input, 0x20), mul(inputSize, 0x20), out, 0x20)
			switch success case 0 { invalid }
		}
		require(success);
		return out[0] != 0;
	}

	function pairingProd2(G1Point a1, G2Point a2, G1Point b1, G2Point b2) constant internal returns (bool) {
		G1Point[] memory p1 = new G1Point[](2);
		G2Point[] memory p2 = new G2Point[](2);
		p1[0] = a1;
		p1[1] = b1;
		p2[0] = a2;
		p2[1] = b2;
		return pairing(p1, p2);
	}

}
