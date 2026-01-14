var __extends = (this && this.__extends) || (function () {
    var extendStatics = function (d, b) {
        extendStatics = Object.setPrototypeOf ||
            ({ __proto__: [] } instanceof Array && function (d, b) { d.__proto__ = b; }) ||
            function (d, b) { for (var p in b) if (Object.prototype.hasOwnProperty.call(b, p)) d[p] = b[p]; };
        return extendStatics(d, b);
    };
    return function (d, b) {
        if (typeof b !== "function" && b !== null)
            throw new TypeError("Class extends value " + String(b) + " is not a constructor or null");
        extendStatics(d, b);
        function __() { this.constructor = d; }
        d.prototype = b === null ? Object.create(b) : (__.prototype = b.prototype, new __());
    };
})();
var Person = /** @class */ (function () {
    function Person(name, age) {
        this.name = name;
        this.age = age;
    }
    Person.prototype.whoami = function () {
        console.log("".concat(this.name, ", and my age is ").concat(this.age));
    };
    return Person;
}());
var BadPerson = /** @class */ (function (_super) {
    __extends(BadPerson, _super);
    function BadPerson(name, age, bad_things) {
        if (bad_things === void 0) { bad_things = []; }
        var _this = _super.call(this, name, age) || this;
        _this.bad_things = [];
        //this.name = "Cool boy"
        _this.bad_things = bad_things;
        return _this;
    }
    BadPerson.prototype.whoami = function () {
        _super.prototype.whoami.call(this);
        console.log("By the wat, I am bad person. My bad stufs are: \n ", this.bad_things);
    };
    return BadPerson;
}(Person));
var dima = new BadPerson("Dima", 14, ["smoking"]);
dima.whoami();
