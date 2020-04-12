pragma solidity ^0.4.24;

contract scheme{

    struct cipheri{
        uint256[2] c1;
        uint256[12] c2;
        uint256[12] c3;
        uint256[12] c4;
    }

    enum State {
        init, twsent, rksent, tksent, ciphersent, paid, closed
    }


    uint256[2] private buyerpk;
    address private buyer;
    uint256[2] private sellerpk;
    address private seller;
    address private cloud;
    uint256[4] private TW;
    uint256[2] private RK;
    uint256[4] private TK;
    cipheri private CIPHER;
    uint256 private value;
    uint256 public WEITOETH  = 1000000000000000000;
    uint256 public WITHGRT   = 1500000000000000000;
    uint256 public FORCLOUD  = 100000000000000000;
    uint256 public FORSELLER = 900000000000000000;
    uint256 public FORBUYER  = 500000000000000000;
    State private state;



    constructor() public payable{
        state = State.init;
        cloud = msg.sender;
    }

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
        require(msg.value == mul(value, WITHGRT), "not enough money");
        _;
    }


    event twsent();
    event rksent();
    event tksent();
    event ciphersent();
    event purchase();
    event confirm();


    function mul(uint256 a, uint256 b) internal pure returns(uint256){
        if (a == 0){
            return 0;
        }
        uint256 c = a * b;
        require(c / a == b);
        return c;
    }

    function Search(uint256[2] bpk, uint256[4] tw)
    public
    inState(State.init)
    {
        emit twsent();
        state = State.twsent;
        buyer = msg.sender;
        buyerpk = bpk;
        TW = tw;
    }

    function PermitSearch(uint256[2] spk, uint256[2] rk)
    public
    inState(State.twsent)
    {
        emit rksent();
        state = State.rksent;
        seller = msg.sender;
        sellerpk = spk;
        RK = rk;
    }

    function PermitReEnc(uint256 v, uint256[4] tk)
    public
    selleronly
    inState(State.rksent)
    {
        emit tksent();
        value = v;
        state = State.tksent;
        TK = tk;
    }

    function SendCipher(uint256[2] c1, uint256[12] c2, uint256[12] c3, uint256[12] c4)
    public
    cloudonly
    inState(State.tksent)
    {
        emit ciphersent();
        state = State.ciphersent;
        CIPHER.c1 = c1;
        CIPHER.c2 = c2;
        CIPHER.c3 = c3;
        CIPHER.c4 = c4;
    }

    function Purchase()
    public
    inState(State.ciphersent)
    buyeronly() enoughmoney()
    payable
    {
        emit purchase();
        state = State.paid;
    }

    function GetCipherC1()
    public
    view
    inState(State.paid)
    buyeronly
    returns(uint256[2])
    {
        return CIPHER.c1;
    }

    function GetCipherC2()
    public
    view
    inState(State.paid)
    buyeronly
    returns(uint256[12])
    {
        return CIPHER.c2;
    }

    function GetCipherC3()
    public
    view
    inState(State.paid)
    buyeronly
    returns(uint256[12])
    {
        return CIPHER.c3;
    }

    function GetCipherC4()
    public
    view
    inState(State.paid)
    buyeronly
    returns(uint256[12])
    {
        return CIPHER.c4;
    }

    function Confirm()
    public
    inState(State.paid)
    buyeronly
    {
        emit confirm();
        state = State.closed;
        seller.transfer(mul(value, FORSELLER));
        cloud.transfer(mul(value, FORCLOUD));
        buyer.transfer(mul(value, FORBUYER));
    }

    function GetState()
    public
    view
    returns(State)
    {
        return (state);
    }
}
