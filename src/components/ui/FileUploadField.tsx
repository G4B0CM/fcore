'use client';

import React, { useMemo, useRef, useState } from 'react';
import { FileUpload, FileUploadHeaderTemplateOptions, FileUploadSelectEvent, FileUploadUploadEvent, ItemTemplateOptions } from 'primereact/fileupload';
import { ProgressBar } from 'primereact/progressbar';

export type FilesValidator = (files: File[]) => string | null;

export type FileUploadFieldProps = {
    name?: string;
    url?: string;
    multiple?: boolean;
    accept?: string;
    maxFileSize?: number;
    auto?: boolean;
    customHeader?: (opts: FileUploadHeaderTemplateOptions, totalSize: number, formatted: string) => React.ReactNode;
    itemTemplate?: (file: File, opts: ItemTemplateOptions) => React.ReactNode;
    emptyTemplate?: React.ReactNode;
    chooseOptions?: any;
    uploadOptions?: any;
    cancelOptions?: any;
    className?: string;
    disabled?: boolean;
    onSelect?: (files: File[]) => void;
    onUpload?: (files: File[]) => void;
    onClear?: () => void;
    validate?: FilesValidator | FilesValidator[];
    showError?: boolean;
};

export default function FileUploadField(props: FileUploadFieldProps) {
    const {
        name, url, multiple, accept, maxFileSize, auto,
        customHeader, itemTemplate, emptyTemplate,
        chooseOptions, uploadOptions, cancelOptions,
        className, disabled, onSelect, onUpload, onClear,
        validate, showError = true
    } = props;

    const ref = useRef<any>(null);
    const [totalSize, setTotalSize] = useState(0);
    const [files, setFiles] = useState<File[]>([]);
    const [error, setError] = useState<string | null>(null);

    const validators = useMemo(() => {
        if (!validate) return [] as FilesValidator[];
        return Array.isArray(validate) ? validate : [validate];
    }, [validate]);

    const runValidation = (list: File[]) => {
        for (const v of validators) {
            const res = v(list);
            if (res) return res;
        }
        return null;
    };

    const headerTemplate = (opts: FileUploadHeaderTemplateOptions) => {
        const value = totalSize / (maxFileSize ? maxFileSize : 1);
        const formatted = ref.current ? ref.current.formatSize(totalSize) : '0 B';
        if (customHeader) return customHeader(opts, totalSize, formatted);
        const { className, chooseButton, uploadButton, cancelButton } = opts;
        return (
            <div className={className} style={{ backgroundColor: 'transparent', display: 'flex', alignItems: 'center' }}>
                {chooseButton}
                {uploadButton}
                {cancelButton}
                <div className="flex align-items-center gap-3 ml-auto">
                    <span>{formatted}{maxFileSize ? ` / ${ref.current?.formatSize(maxFileSize)}` : ''}</span>
                    <ProgressBar value={Math.min(100, value * 100)} showValue={false} style={{ width: '10rem', height: '12px' }} />
                </div>
            </div>
        );
    };

    const onTemplateSelect = (e: FileUploadSelectEvent) => {
        const list = Array.from(e.files ?? []);
        const size = list.reduce((acc, f) => acc + (f.size || 0), totalSize);
        setFiles((prev) => [...prev, ...list]);
        setTotalSize(size);
        setError(runValidation([...files, ...list]));
        onSelect?.(list);
    };

    const onTemplateUpload = (e: FileUploadUploadEvent) => {
        const uploaded = Array.from(e.files ?? []);
        setFiles(uploaded);
        setTotalSize(uploaded.reduce((acc, f) => acc + (f.size || 0), 0));
        setError(runValidation(uploaded));
        onUpload?.(uploaded);
    };

    const onTemplateClear = () => {
        setFiles([]);
        setTotalSize(0);
        setError(runValidation([]));
        onClear?.();
    };

    const itemTpl = (inFile: object, opts: ItemTemplateOptions) => {
        const file = inFile as File;
        if (itemTemplate) return itemTemplate(file, opts);
        return (
            <div className="flex align-items-center flex-wrap w-full">
                <div className="flex align-items-center" style={{ width: '50%' }}>
                    <span className="flex flex-column text-left ml-3">
                        {file.name}
                        <small>{new Date().toLocaleString()}</small>
                    </span>
                </div>
                <span className="ml-auto mr-2">{opts.formatSize}</span>
                <button type="button" className="p-button p-button-text p-button-danger p-button-rounded" onClick={() => opts.onRemove(file)}>
                    <i className="pi pi-times" />
                </button>
            </div>
        );
    };

    return (
        <div className={className}>
            <FileUpload
                ref={ref}
                name={name ?? 'files[]'}
                url={url}
                multiple={multiple}
                accept={accept}
                maxFileSize={maxFileSize}
                auto={auto}
                onSelect={onTemplateSelect}
                onUpload={onTemplateUpload}
                onError={onTemplateClear}
                onClear={onTemplateClear}
                headerTemplate={headerTemplate}
                itemTemplate={itemTpl}
                emptyTemplate={emptyTemplate}
                chooseOptions={chooseOptions}
                uploadOptions={uploadOptions}
                cancelOptions={cancelOptions}
                disabled={disabled}
            />
            {showError && error && <small className="p-error block mt-2">{error}</small>}
        </div>
    );
}
