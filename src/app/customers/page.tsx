'use client';

import React, { useEffect, useMemo, useRef, useState } from 'react';
import DataTablePro, { ColumnDef } from '@/components/ui/DataTablePro';
import RangeNumberFilter from '@/components/ui/RangeNumberFilter';
import { registerNumberRangeFilter } from '@/components/ui/registerFilters';
import { BoolIconCell, TagCell, statusSeverity } from '@/components/ui/Cells';
import AppButton from '@/components/ui/AppButton';
import { Dropdown, DropdownChangeEvent } from 'primereact/dropdown';
import { MultiSelect, MultiSelectChangeEvent } from 'primereact/multiselect';
import { Toast } from 'primereact/toast';
import { DataTableFilterMeta } from 'primereact/datatable';
import Image from 'next/image';

type Representative = { name: string; image: string };
type Country = { name: string; code: string };
type Customer = {
    id: number;
    name: string;
    country: Country;
    company: string;
    date: Date;
    status: string;
    verified: boolean;
    activity: number;
    representative: Representative;
    balance: number;
};

registerNumberRangeFilter();

const reps: Representative[] = [
    { name: 'Amy Elsner', image: 'amyelsner.png' },
    { name: 'Anna Fali', image: 'annafali.png' },
    { name: 'Asiya Javayant', image: 'asiyajavayant.png' },
    { name: 'Bernardo Dominic', image: 'bernardodominic.png' },
    { name: 'Elwin Sharvill', image: 'elwinsharvill.png' },
    { name: 'Ioni Bowcher', image: 'ionibowcher.png' },
    { name: 'Ivan Magalhaes', image: 'ivanmagalhaes.png' },
    { name: 'Onyama Limba', image: 'onyamalimba.png' },
    { name: 'Stephen Shaw', image: 'stephenshaw.png' },
    { name: 'XuXue Feng', image: 'xuxuefeng.png' }
];

const statuses = ['unqualified', 'qualified', 'new', 'negotiation', 'renewal'];

function avatarUrl(file: string) {
    return `https://primefaces.org/cdn/primereact/images/avatar/${file}`;
}
function flagUrl(code: string) {
    return `https://primefaces.org/cdn/primereact/images/flag/flag_placeholder.png`;
}

export default function CustomersPage() {
    const toast = useRef<Toast>(null);
    const [loading, setLoading] = useState(true);
    const [customers, setCustomers] = useState<Customer[]>([]);
    const [filters, setFilters] = useState<DataTableFilterMeta>({
        global: { value: null, matchMode: 'contains' },
        name: { value: null, matchMode: 'startsWith' },
        'country.name': { value: null, matchMode: 'startsWith' },
        representative: { value: null, matchMode: 'in' },
        activity: { value: null, matchMode: 'custom' },
        status: { value: null, matchMode: 'equals' },
        verified: { value: null, matchMode: 'equals' }
    });

    useEffect(() => {
        const mock: Customer[] = Array.from({ length: 40 }).map((_, i) => {
            const countryCodes = ['AU', 'BR', 'CN', 'EG', 'FR', 'DE', 'IN', 'JP', 'ES', 'US'];
            const cidx = i % countryCodes.length;
            return {
                id: i + 1,
                name: `Customer ${i + 1}`,
                country: { name: ['Australia', 'Brazil', 'China', 'Egypt', 'France', 'Germany', 'India', 'Japan', 'Spain', 'United States'][cidx], code: countryCodes[cidx].toLowerCase() },
                company: `Company ${i + 1}`,
                date: new Date(2024, (i % 12), 1 + (i % 28)),
                status: statuses[i % statuses.length],
                verified: i % 2 === 0,
                activity: Math.floor(Math.random() * 100),
                representative: reps[i % reps.length],
                balance: Math.round(Math.random() * 10000) / 100
            };
        });
        setTimeout(() => {
            setCustomers(mock);
            setLoading(false);
        }, 600);
    }, []);

    const columns = useMemo<ColumnDef<Customer>[]>(() => {
        return [
            { field: 'name', header: 'Name', sortable: true, filter: true, filterPlaceholder: 'Search by name', style: { minWidth: '12rem' } },
            {
                header: 'Country',
                field: 'country.name',
                sortable: true,
                filter: true,
                filterPlaceholder: 'Search by country',
                style: { minWidth: '12rem' },
                body: (row) => (
                    <div className="flex align-items-center gap-2">
                        <Image alt="flag" src={flagUrl(row.country.code)} width={24} height={16} className={`flag flag-${row.country.code}`} />
                        <span>{row.country.name}</span>
                    </div>
                )
            },
            {
                header: 'Agent',
                field: 'representative',
                showFilterMenu: false,
                style: { minWidth: '14rem' },
                filter: true,
                filterElement: (options: any) => (
                    <MultiSelect
                        value={options.value}
                        options={reps}
                        itemTemplate={(o: Representative) => (
                            <div className="flex align-items-center gap-2">
                                <Image alt={o.name} src={avatarUrl(o.image)} width={32} height={32} />
                                <span>{o.name}</span>
                            </div>
                        )}
                        onChange={(e: MultiSelectChangeEvent) => options.filterApplyCallback(e.value)}
                        optionLabel="name"
                        placeholder="Any"
                        className="p-column-filter"
                        maxSelectedLabels={1}
                        style={{ minWidth: '14rem' }}
                    />
                ),
                body: (row) => (
                    <div className="flex align-items-center gap-2">
                        <Image alt={row.representative.name} src={avatarUrl(row.representative.image)} width={32} height={32} />
                        <span>{row.representative.name}</span>
                    </div>
                )
            },
            {
                header: 'Activity (Range)',
                field: 'activity',
                showFilterMenu: false,
                style: { minWidth: '14rem' },
                filter: true,
                filterElement: (options: any) => (
                    <RangeNumberFilter value={options.value} onChange={(val) => options.filterApplyCallback(val)} />
                )
            },
            {
                field: 'status',
                header: 'Status',
                showFilterMenu: false,
                style: { minWidth: '12rem' },
                filter: true,
                filterElement: (options: any) => (
                    <Dropdown
                        value={options.value}
                        options={statuses}
                        onChange={(e: DropdownChangeEvent) => options.filterApplyCallback(e.value)}
                        itemTemplate={(opt: string) => <TagCell value={opt} severity={statusSeverity(opt) as any} />}
                        placeholder="Select One"
                        className="p-column-filter"
                        showClear
                        style={{ minWidth: '12rem' }}
                    />
                ),
                body: (row) => <TagCell value={row.status} severity={statusSeverity(row.status) as any} />
            },
            {
                field: 'verified',
                header: 'Verified',
                dataType: 'boolean',
                style: { minWidth: '6rem' },
                filter: true,
                filterElement: (options: any) => <TriState options={options} />,
                body: (row) => <BoolIconCell value={row.verified} />
            },
            {
                header: 'Actions',
                body: (row) => (
                    <div className="flex gap-2">
                        <AppButton icon="pi pi-eye" severity="info" ariaLabel="View" onClick={() => toast.current?.show({ severity: 'info', summary: 'View', detail: `#${row.id}`, life: 1800 })} />
                        <AppButton icon="pi pi-pencil" severity="warning" ariaLabel="Edit" onClick={() => toast.current?.show({ severity: 'warn', summary: 'Edit', detail: `#${row.id}`, life: 1800 })} />
                        <AppButton icon="pi pi-trash" severity="danger" ariaLabel="Delete" onClick={() => toast.current?.show({ severity: 'error', summary: 'Delete', detail: `#${row.id}`, life: 1800 })} />
                    </div>
                )
            }
        ];
    }, []);

    function TriState({ options }: { options: any }) {
        return <div className="p-inputswitch p-inputwrapper">
            <Dropdown
                value={options.value}
                options={[
                    { label: 'Any', value: null },
                    { label: 'True', value: true },
                    { label: 'False', value: false }
                ]}
                onChange={(e: DropdownChangeEvent) => options.filterApplyCallback(e.value)}
                className="p-column-filter"
                style={{ minWidth: '8rem' }}
            />
        </div>;
    }

    return (
        <div className="p-4">
            <Toast ref={toast} position="bottom-right" />
            <DataTablePro<Customer>
                value={customers}
                columns={columns}
                loading={loading}
                dataKey="id"
                paginator
                rows={10}
                filters={filters}
                onFilter={(e) => setFilters(e.filters)}
                globalFilterFields={['name', 'country.name', 'representative.name', 'status']}
                className="shadow-1 surface-card p-2 border-round"
                emptyMessage="No customers found."
            />
        </div>
    );
}
