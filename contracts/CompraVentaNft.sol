pragma solidity ^0.6.6;

//-------------ORACLES---------------------------------

//This oracle will help us to create our NFT in the ERC721 standard
import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
//This oracle will give us the USD-ETH exchange rate
import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
//This oracle will help us with some math problem limitations of the compiler (not an issue in  0.8.0 and beyond)
import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol";

contract CompraVentaNft is ERC721 {
    using SafeMathChainlink for uint256;
    //-------------VARIABLES---------------------------

    address private owner; // the Contract's owner
    uint256 public tokenCounter; // control the number of deployed NFTS
    /*OpenZeppelin already has some useful variables
        such as _tokenOwner which tell us which token belong to whom */
    uint256 public usdPrice; //The Usd price of the NFT
    AggregatorV3Interface internal ethUsdPriceFeed;
    /* Chainlink will give us constant updates on the
        USD-ETH exchange rate */
    enum SALE_STATE {
        OPEN,
        CLOSED
    }
    SALE_STATE public saleState;

    /* This will help us to create
        an equivalent function of IsStopped,
        this way of doing it, is far more safer 
        and practical than using a boolean (true-false)
        OPEN= 0
        CLOSED=1
        */
    //-------------CONSTRUCTOR---------------------------
    constructor(address _priceFeed) public ERC721("Lesiones:Paz", "PAZ") {
        tokenCounter = 0;
        owner = msg.sender;
        usdPrice = 2 * (10**18);
        /*We msut muliplie the usd value ($2) by 18 zeroes 
        as we are managing the contract in WEI (a fraction of ETH) */
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeed);
        saleState = SALE_STATE.OPEN;
    }

    //-------------MODIFIER--------------------------
    modifier onlyOwner() {
        /*Through this modifier we'll be able to verify the contract's propiety*/
        require(
            msg.sender == owner,
            "You must be the owner in order to excecute this function"
        );
        _;
    }

    //||||||||||||FUNCTION 1 CREATE AN NFT|||||||||||||||||||||||

    function createCollectible() public payable returns (uint256) {
        require(
            saleState == SALE_STATE.OPEN,
            "The NFT sale is currently closed"
        );
        require(
            tokenCounter < 21,
            "We're sorry, There won't be a new minting of NFT"
        );

        require(
            msg.value >= getPrice(),
            "You must pay the ETH to USD value of the NFT"
        );
        /* We find in this function two things:
        1. The object of the contract : the transfer of the thing
        2. The requirements to perfect (to validly celebrate) the contract:
            a. The thing
            b. The price
        */

        //We use token counter to assing a value to the will be minted NFT
        uint256 newTokenId = tokenCounter;
        //second verification before minting the nft
        if (address(this).balance >= getPrice() && msg.value >= getPrice()) {
            _safeMint(msg.sender, newTokenId); // Through the _mint function (Taken from OpenZeppelin) we'll asSing the propiety of the NFT to the new buyer
            tokenCounter = tokenCounter + 1; //We update the token counter variable
        } else {
            "You should send enough ether to mint the NFT";
        }

        if (msg.sender != owner) {
            approve(owner, newTokenId);
        }
        // putting this transfer here secures that the account balance always starts at 0 before minting
        payable(owner).transfer(address(this).balance); //After a succesful mint, the owner-artist will be payed in ETH
        return newTokenId;
    }

    //||||||||||||FUNCTION 2 SET IMAGE|||||||||||||||||||||||
    function setTokenURI(uint256 tokenId, string memory _tokenURI) public {
        // This functions sets the image associated to the NFT
        require(
            _isApprovedOrOwner(_msgSender(), tokenId), //is aproved or owner checks ownership
            "ERC721: caller is not owner nor approved"
        );
        _setTokenURI(tokenId, _tokenURI);
    }

    //||||||||||||FUNCTION 2 USD-ETHER|||||||||||||||||||||||

    function getPrice() public view returns (uint256) {
        (
            ,
            /*This function is provided by the chainlink oracles,
            nevertheless, we only require the exchange rate of USD to ETH
            so we'll leave some blanks that were assigned to other variables*/
            int256 price,
            ,
            ,

        ) = ethUsdPriceFeed.latestRoundData();
        uint256 AdjustedPrice = uint256(price) * 10**10;
        /*We ought to multiply 10**10, so the final price is given
        with 18 decimals, because the price given by the oracle 
        only has 8 decimal places.
        */
        // usd: $2,$3000/eth
        //2*100000/3000
        uint256 costToEnter = (usdPrice * 10**18) / AdjustedPrice;
        return costToEnter;
    }

    //||||||||||||FUNCTION 3 OPEN SALE|||||||||||||||||||||||

    function startSale() public onlyOwner {
        require(
            tokenCounter < 21,
            "you've already sold the target sale of NFTS"
        );
        require(
            saleState == SALE_STATE.CLOSED,
            "You're already selling your NFTS"
        );
        saleState = SALE_STATE.OPEN;
    }

    //||||||||||||FUNCTION 4 CLOSE SALE|||||||||||||||||||||||
    function endSale() public onlyOwner {
        require(saleState == SALE_STATE.OPEN, "The sale is already closed");
        saleState = SALE_STATE.CLOSED;
    }

    //||||||||||||FUNCTION 5 UPDATE PRICE|||||||||||||||||||||||
    function updatePrice(uint256 _usdPrice) public onlyOwner {
        usdPrice = _usdPrice * (10**18);
    }

    //||||||||||||FUNCTION 6 TARGET SALE|||||||||||||||||||||||
    function nftTargetSale() public view returns (string memory) {
        return string("Our Target Sale are 20 NFTS");
    }
}
