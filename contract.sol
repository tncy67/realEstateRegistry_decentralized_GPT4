// SPDX-License-Identifier: GPL-3.0
pragma solidity ^0.8.0;

contract RealEstateMarket {
    struct Property {
        address owner;
        uint256 price;
        string propertyDetails;
        uint256[] transactionHistory;
    }

    mapping(uint256 => Property) public properties;
    uint256 public propertyId;

    event PropertyRegistered(uint256 indexed propertyId, address indexed owner, uint256 price, string propertyDetails);
    event PropertyPurchased(uint256 indexed propertyId, address indexed previousOwner, address indexed newOwner, uint256 price);

    function registerProperty(uint256 price, string memory propertyDetails) public {
        require(price > 0, "Price must be greater than zero.");
        properties[propertyId] = Property(msg.sender, price, propertyDetails, new uint256[](0));

        emit PropertyRegistered(propertyId, msg.sender, price, propertyDetails);
        propertyId++;
    }

    function buyProperty(uint256 _propertyId) public payable {
        Property storage property = properties[_propertyId];

        require(msg.sender != property.owner, "You cannot buy your own property.");
        require(msg.value >= property.price, "Insufficient funds sent for the purchase.");

        uint256 refundAmount = msg.value - property.price;
        if (refundAmount > 0) {
            payable(msg.sender).transfer(refundAmount);
        }

        address previousOwner = property.owner;
        uint256 purchasePrice = property.price;

        property.transactionHistory.push(purchasePrice);
        property.owner = msg.sender;
        property.price = 0;

        payable(previousOwner).transfer(purchasePrice);

        emit PropertyPurchased(_propertyId, previousOwner, msg.sender, purchasePrice);
    }

    function updatePropertyPrice(uint256 _propertyId, uint256 newPrice) public {
        require(newPrice > 0, "Price must be greater than zero.");
        Property storage property = properties[_propertyId];
        require(msg.sender == property.owner, "Only the owner can update the price.");

        property.price = newPrice;
    }

    function getPropertyTransactionHistory(uint256 _propertyId) public view returns (uint256[] memory) {
        return properties[_propertyId].transactionHistory;
    }
}
