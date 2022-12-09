pragma solidity ^0.5.0;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v2.5.0/contracts/token/ERC721/ERC721Full.sol";

contract BootcampCertificate is ERC721Full {
    constructor() public ERC721Full("BootcampCertificate", "BCC") {}

    struct Certificate {
        string name;
        string completionDate;
        string certJson;
    }

    mapping(uint256 => Certificate) public certifcateList;

    function imageUri(uint256 tokenId)
        public
        view
        returns (string memory imageJson)
    {
        return certifcateList[tokenId].certJson;
    }

    function registerCertificate(
        address owner,
        string memory name,
        string memory completionDate,
        string memory tokenURI,
        string memory tokenJSON
    ) public returns (uint256) {
        uint256 tokenId = totalSupply();
        _mint(owner, tokenId);
        _setTokenURI(tokenId, tokenURI);
        certifcateList[tokenId] = Certificate(name, completionDate, tokenJSON);
    }
}
