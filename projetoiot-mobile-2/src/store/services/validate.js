
// ------------------------- CHAIN OF RESPONSABILITY -------------------------


class AbstractHandler {
    nextHandler = null;

    setNext(handler) {
        this.nextHandler = handler;
        return handler;
    }

    async handle(request) {
        if (this.nextHandler) {
            return this.nextHandler.handle(request);
        }
        return null
    }
}

class ValidateNameHandler extends AbstractHandler {
    async handle(request) {
        if(!request.user_name) throw Error('Name Needed');
        if(request.user_name.length > 30) throw Error('Name size exceeded - limit 30 characters');

        return super.handle(request);

    }
}

class ValidateImageHandler extends AbstractHandler {
    async handle(request)  {
        if(!request.image) throw Error('Image Needed');

        return super.handle(request);

    }
}

export class ValidadeAndSubmitFormChain {
    start (data) {
        const name = new ValidateNameHandler();
        const image = new ValidateImageHandler();

        name.setNext(image)

        return name.handle(data);
    }
}

