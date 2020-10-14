// 串行Promise

function resolve(...args) {
    return new Promise(function(resolve, reject) {
        setTimeout(function() {
             resolve(...args);
        }, 200);
    });
}

async function test() {
	var start = Date.now();
    for (var i = 0; i < 10; i++) {
        let res = await resolve(i * i);
        console.log(Date.now(), res);
    }
    var used = Date.now() - start;
    console.log("used time: %d ms", used);
}

test();
