/* tslint:disable */
/* eslint-disable */
/**
 * Image Codex
 * No description provided (generated by Openapi Generator https://github.com/openapitools/openapi-generator)
 *
 * The version of the OpenAPI document: 0.1.0
 * 
 *
 * NOTE: This class is auto generated by OpenAPI Generator (https://openapi-generator.tech).
 * https://openapi-generator.tech
 * Do not edit the class manually.
 */


import { Configuration } from './configuration';
import globalAxios, { AxiosPromise, AxiosInstance } from 'axios';
// Some imports not used depending on template conditions
// @ts-ignore
import { DUMMY_BASE_URL, assertParamExists, setApiKeyToObject, setBasicAuthToObject, setBearerAuthToObject, setOAuthToObject, setSearchParams, serializeDataIfNeeded, toPathString, createRequestFunction } from './common';
// @ts-ignore
import { BASE_PATH, COLLECTION_FORMATS, RequestArgs, BaseAPI, RequiredError } from './base';

/**
 * 
 * @export
 * @interface ApiFile
 */
export interface ApiFile {
    /**
     * 
     * @type {string}
     * @memberof ApiFile
     */
    name?: string;
    /**
     * 
     * @type {string}
     * @memberof ApiFile
     */
    type?: string;
    /**
     * 
     * @type {string}
     * @memberof ApiFile
     */
    base64: string;
}
/**
 * 
 * @export
 * @interface ComposedImage
 */
export interface ComposedImage {
    /**
     * 
     * @type {string}
     * @memberof ComposedImage
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof ComposedImage
     */
    url: string;
    /**
     * 
     * @type {number}
     * @memberof ComposedImage
     */
    x: number;
    /**
     * 
     * @type {number}
     * @memberof ComposedImage
     */
    y: number;
    /**
     * 
     * @type {number}
     * @memberof ComposedImage
     */
    width: number;
    /**
     * 
     * @type {number}
     * @memberof ComposedImage
     */
    height: number;
}
/**
 * 
 * @export
 * @interface CursorPageResponseImage
 */
export interface CursorPageResponseImage {
    /**
     * 
     * @type {Array<ResponseImage>}
     * @memberof CursorPageResponseImage
     */
    items: Array<ResponseImage>;
    /**
     * 
     * @type {number}
     * @memberof CursorPageResponseImage
     */
    total: number;
    /**
     * 
     * @type {string}
     * @memberof CursorPageResponseImage
     */
    next?: string;
    /**
     * 
     * @type {number}
     * @memberof CursorPageResponseImage
     */
    size: number;
}
/**
 * 
 * @export
 * @interface HTTPValidationError
 */
export interface HTTPValidationError {
    /**
     * 
     * @type {Array<ValidationError>}
     * @memberof HTTPValidationError
     */
    detail?: Array<ValidationError>;
}
/**
 * 
 * @export
 * @interface RequestComposition
 */
export interface RequestComposition {
    /**
     * 
     * @type {string}
     * @memberof RequestComposition
     */
    name: string;
    /**
     * 
     * @type {number}
     * @memberof RequestComposition
     */
    width: number;
    /**
     * 
     * @type {number}
     * @memberof RequestComposition
     */
    height: number;
    /**
     * 
     * @type {Array<number>}
     * @memberof RequestComposition
     */
    background_color?: Array<number>;
    /**
     * 
     * @type {Array<ComposedImage>}
     * @memberof RequestComposition
     */
    images: Array<ComposedImage>;
}
/**
 * 
 * @export
 * @interface ResponseImage
 */
export interface ResponseImage {
    /**
     * 
     * @type {string}
     * @memberof ResponseImage
     */
    id: string;
    /**
     * 
     * @type {string}
     * @memberof ResponseImage
     */
    name: string;
    /**
     * 
     * @type {string}
     * @memberof ResponseImage
     */
    url: string;
    /**
     * 
     * @type {number}
     * @memberof ResponseImage
     */
    width: number;
    /**
     * 
     * @type {number}
     * @memberof ResponseImage
     */
    height: number;
    /**
     * 
     * @type {Array<string>}
     * @memberof ResponseImage
     */
    tags: Array<string>;
    /**
     * 
     * @type {string}
     * @memberof ResponseImage
     */
    author: string;
    /**
     * 
     * @type {string}
     * @memberof ResponseImage
     */
    license: string;
}
/**
 * 
 * @export
 * @interface ValidationError
 */
export interface ValidationError {
    /**
     * 
     * @type {Array<string>}
     * @memberof ValidationError
     */
    loc: Array<string>;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    msg: string;
    /**
     * 
     * @type {string}
     * @memberof ValidationError
     */
    type: string;
}

/**
 * DefaultApi - axios parameter creator
 * @export
 */
export const DefaultApiAxiosParamCreator = function (configuration?: Configuration) {
    return {
        /**
         * 
         * @summary Create Composition
         * @param {RequestComposition} requestComposition 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createCompositionCompositionsPost: async (requestComposition: RequestComposition, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'requestComposition' is not null or undefined
            assertParamExists('createCompositionCompositionsPost', 'requestComposition', requestComposition)
            const localVarPath = `/compositions`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(requestComposition, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Create Image
         * @param {ApiFile} apiFile 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createImageImagesPost: async (apiFile: ApiFile, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'apiFile' is not null or undefined
            assertParamExists('createImageImagesPost', 'apiFile', apiFile)
            const localVarPath = `/images`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'POST', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            localVarHeaderParameter['Content-Type'] = 'application/json';

            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};
            localVarRequestOptions.data = serializeDataIfNeeded(apiFile, localVarRequestOptions, configuration)

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Get Image
         * @param {string} imageIds 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getImageImagesImageIdsGet: async (imageIds: string, options: any = {}): Promise<RequestArgs> => {
            // verify required parameter 'imageIds' is not null or undefined
            assertParamExists('getImageImagesImageIdsGet', 'imageIds', imageIds)
            const localVarPath = `/images/{image_ids}`
                .replace(`{${"image_ids"}}`, encodeURIComponent(String(imageIds)));
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Get Images
         * @param {Array<string>} [tags] 
         * @param {string} [author] 
         * @param {string} [next] 
         * @param {number} [size] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getImagesImagesGet: async (tags?: Array<string>, author?: string, next?: string, size?: number, options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/images`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;

            if (tags) {
                localVarQueryParameter['tags'] = tags;
            }

            if (author !== undefined) {
                localVarQueryParameter['author'] = author;
            }

            if (next !== undefined) {
                localVarQueryParameter['next'] = next;
            }

            if (size !== undefined) {
                localVarQueryParameter['size'] = size;
            }


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
        /**
         * 
         * @summary Root
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        rootGet: async (options: any = {}): Promise<RequestArgs> => {
            const localVarPath = `/`;
            // use dummy base URL string because the URL constructor only accepts absolute URLs.
            const localVarUrlObj = new URL(localVarPath, DUMMY_BASE_URL);
            let baseOptions;
            if (configuration) {
                baseOptions = configuration.baseOptions;
            }

            const localVarRequestOptions = { method: 'GET', ...baseOptions, ...options};
            const localVarHeaderParameter = {} as any;
            const localVarQueryParameter = {} as any;


    
            setSearchParams(localVarUrlObj, localVarQueryParameter, options.query);
            let headersFromBaseOptions = baseOptions && baseOptions.headers ? baseOptions.headers : {};
            localVarRequestOptions.headers = {...localVarHeaderParameter, ...headersFromBaseOptions, ...options.headers};

            return {
                url: toPathString(localVarUrlObj),
                options: localVarRequestOptions,
            };
        },
    }
};

/**
 * DefaultApi - functional programming interface
 * @export
 */
export const DefaultApiFp = function(configuration?: Configuration) {
    const localVarAxiosParamCreator = DefaultApiAxiosParamCreator(configuration)
    return {
        /**
         * 
         * @summary Create Composition
         * @param {RequestComposition} requestComposition 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createCompositionCompositionsPost(requestComposition: RequestComposition, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<ApiFile>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createCompositionCompositionsPost(requestComposition, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Create Image
         * @param {ApiFile} apiFile 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async createImageImagesPost(apiFile: ApiFile, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.createImageImagesPost(apiFile, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Get Image
         * @param {string} imageIds 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getImageImagesImageIdsGet(imageIds: string, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<Array<ResponseImage>>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getImageImagesImageIdsGet(imageIds, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Get Images
         * @param {Array<string>} [tags] 
         * @param {string} [author] 
         * @param {string} [next] 
         * @param {number} [size] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async getImagesImagesGet(tags?: Array<string>, author?: string, next?: string, size?: number, options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<CursorPageResponseImage>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.getImagesImagesGet(tags, author, next, size, options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
        /**
         * 
         * @summary Root
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        async rootGet(options?: any): Promise<(axios?: AxiosInstance, basePath?: string) => AxiosPromise<any>> {
            const localVarAxiosArgs = await localVarAxiosParamCreator.rootGet(options);
            return createRequestFunction(localVarAxiosArgs, globalAxios, BASE_PATH, configuration);
        },
    }
};

/**
 * DefaultApi - factory interface
 * @export
 */
export const DefaultApiFactory = function (configuration?: Configuration, basePath?: string, axios?: AxiosInstance) {
    const localVarFp = DefaultApiFp(configuration)
    return {
        /**
         * 
         * @summary Create Composition
         * @param {RequestComposition} requestComposition 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createCompositionCompositionsPost(requestComposition: RequestComposition, options?: any): AxiosPromise<ApiFile> {
            return localVarFp.createCompositionCompositionsPost(requestComposition, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Create Image
         * @param {ApiFile} apiFile 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        createImageImagesPost(apiFile: ApiFile, options?: any): AxiosPromise<any> {
            return localVarFp.createImageImagesPost(apiFile, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Get Image
         * @param {string} imageIds 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getImageImagesImageIdsGet(imageIds: string, options?: any): AxiosPromise<Array<ResponseImage>> {
            return localVarFp.getImageImagesImageIdsGet(imageIds, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Get Images
         * @param {Array<string>} [tags] 
         * @param {string} [author] 
         * @param {string} [next] 
         * @param {number} [size] 
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        getImagesImagesGet(tags?: Array<string>, author?: string, next?: string, size?: number, options?: any): AxiosPromise<CursorPageResponseImage> {
            return localVarFp.getImagesImagesGet(tags, author, next, size, options).then((request) => request(axios, basePath));
        },
        /**
         * 
         * @summary Root
         * @param {*} [options] Override http request option.
         * @throws {RequiredError}
         */
        rootGet(options?: any): AxiosPromise<any> {
            return localVarFp.rootGet(options).then((request) => request(axios, basePath));
        },
    };
};

/**
 * DefaultApi - object-oriented interface
 * @export
 * @class DefaultApi
 * @extends {BaseAPI}
 */
export class DefaultApi extends BaseAPI {
    /**
     * 
     * @summary Create Composition
     * @param {RequestComposition} requestComposition 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public createCompositionCompositionsPost(requestComposition: RequestComposition, options?: any) {
        return DefaultApiFp(this.configuration).createCompositionCompositionsPost(requestComposition, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Create Image
     * @param {ApiFile} apiFile 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public createImageImagesPost(apiFile: ApiFile, options?: any) {
        return DefaultApiFp(this.configuration).createImageImagesPost(apiFile, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Get Image
     * @param {string} imageIds 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public getImageImagesImageIdsGet(imageIds: string, options?: any) {
        return DefaultApiFp(this.configuration).getImageImagesImageIdsGet(imageIds, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Get Images
     * @param {Array<string>} [tags] 
     * @param {string} [author] 
     * @param {string} [next] 
     * @param {number} [size] 
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public getImagesImagesGet(tags?: Array<string>, author?: string, next?: string, size?: number, options?: any) {
        return DefaultApiFp(this.configuration).getImagesImagesGet(tags, author, next, size, options).then((request) => request(this.axios, this.basePath));
    }

    /**
     * 
     * @summary Root
     * @param {*} [options] Override http request option.
     * @throws {RequiredError}
     * @memberof DefaultApi
     */
    public rootGet(options?: any) {
        return DefaultApiFp(this.configuration).rootGet(options).then((request) => request(this.axios, this.basePath));
    }
}

